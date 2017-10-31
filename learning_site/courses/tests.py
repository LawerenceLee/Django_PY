from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from .models import Course, Step


class CourseModelTests(TestCase):

    def test_course_creation(self):
        course = Course.objects.create(
            title="Python Regular Expressions",
            description="Learn to write regular expressions in Python."
        )
        now = timezone.now()
        self.assertLess(course.created_at, now)


class StepModelTests(TestCase):

    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='Learn to write tests in Python.'
        )

    def test_step_creation(self):
        step = Step.objects.create(
            title="Introduction to Doctests",
            description="Learn to write docstrings",
            course=self.course
        )
        self.assertIn(step, self.course.step_set.all())


class CourseViewsTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title='Python Testing',
            description='A new course'
        )
        self.course2 = Course.objects.create(
            title='New Course',
            description='A new course'
        )
        self.step = Step.objects.create(
            title='Introduction to DocTests',
            description='Learn to write tests in your docstrings.',
            course=self.course
        )
        self.step2 = Step.objects.create(
            title='Introduction to UnitTests',
            description='Learn to unittests.',
            course=self.course2
        )

    def test_course_list_view(self):
        resp = self.client.get(reverse('courses:course_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.course, resp.context['courses'])
        self.assertIn(self.course2, resp.context['courses'])
        self.assertTemplateUsed(resp, 'courses/course_list.html')
        self.assertContains(resp, self.course.title)

    def test_course_detail_view(self):
        resp = self.client.get(reverse('courses:detail',
                               kwargs={'pk': self.course2.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.course2, resp.context['course'])
        self.assertNotEqual(self.course, resp.context['course'])

    def test_step_detail_view(self):
        resp = self.client.get(reverse('courses:step', kwargs={
                    'course_pk': self.course2.pk,
                    'step_pk': self.step2.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.step2, resp.context['step'])
        self.assertNotEqual(self.step, resp.context['step'])
