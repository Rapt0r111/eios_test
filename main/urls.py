import django
from django.urls import path, re_path
from django.views.decorators.cache import cache_page

from eios_test import settings
from .views import *



urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('lessons/<slug:slug>', LessonPage.as_view(), name='lessons'),
    path('sign-in', SignForm.as_view(), name='sign-in'),
    path('sign-up', SignUp.as_view(), name='sign-up'),
    path('profile', ProfilePage.as_view(), name='profile-page'),
    path('logout', logout_view, name='logout'),
    path('edit/<slug:username>', EditProfile.as_view(), name='edit'),
    path('lesson-view', LessonEditPage.as_view(), name='lesson-view'),
    path('lesson-create', LessonCreate.as_view(), name='lesson-create'),
    path('topic-create/<slug:slug>', LessonChangePage.as_view(), name='topic-create'),
    path('topic-edit/<slug:id>', TopicUpdateForm.as_view(), name='topic-edit'),
]
