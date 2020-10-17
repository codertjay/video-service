from django.shortcuts import render
from django.views.generic import *

from memberships.models import UserMembership
from .models import *


class CourseListView(ListView):
    model = Course
    context_object_name = 'course'
    template_name = 'courses/course_list.html'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'


class LessonDetailView(View):

    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course_qs = Course.objects.filter(slug=course_slug)
        if course_qs.exists():
            course = course_qs.first()

        lesson_qs = course.lessons.filter(slug=lesson_slug)
        if lesson_qs.exists():
            lesson = lesson_qs.first()

        user_membership = UserMembership.objects.filter(user=request.user).first()
        """below we are getting the user memberships type so we can filter what
         to display to the user"""
        user_membership_type = user_membership.membership.membership_type
        course_allowed_membership_types = course.allowed_memberships.all()
        context = {
            'object': None
        }
        if course_allowed_membership_types.filter(membership_type=user_membership_type).exists():
            context = {'objects': lesson}
        return render(request, 'courses/lesson_detail.html', context)
