from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from .views import CourseListView,CourseDetailView,WeekDetailView

app_name='courses'

urlpatterns = [
    path('', CourseListView.as_view(),name='liste'),
    path('<slug>', CourseDetailView.as_view(),name='detail'),
    path('<challenge_slug>/<week_slug>', WeekDetailView.as_view(),name='week_detail'),
]

