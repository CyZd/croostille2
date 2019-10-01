from django.shortcuts import render

from django.views.generic import ListView, DetailView,View
from .models import Challenge, Week

from memberships.models import UserMembership

from django.contrib.auth.models import User

from datetime import datetime,date
from django.utils import formats

def user_is_old(request):
    user_joined_date=formats.date_format(request.user.date_joined, "DATE_FORMAT")
    formated_date=datetime.strptime(user_joined_date,"%B %d,%Y").date()
    current_time=date.today()

    delta=current_time-formated_date

    result=delta.days

    return result

class CourseListView(ListView):
    model=Challenge

class CourseDetailView(DetailView):
    model=Challenge

    def get(self, request, *args,**kwargs):
        user_days=user_is_old(request)
        context={
            'user_days':user_days
            }

        return render(request,"courses/challenge_detail.html",context)

class WeekDetailView(View):

    def get(self, request, challenge_slug,week_slug, *args,**kwargs):

        challenge_queryset=Challenge.objects.filter(slug=challenge_slug)
        if challenge_queryset.exists():
            global challenge
            challenge=challenge_queryset.first()


        week_queryset=challenge.weeks.filter(slug=week_slug)
        if week_queryset.exists():
            global week
            week=week_queryset.first()


        user_membership=UserMembership.objects.filter(user=request.user).first()
        user_membership_type=user_membership.membership.membership_type

        challenge_allowed_membership_type=challenge.allowed_memberships.all()

        context={
            'object':None 
        }

        user_days=user_is_old(request)
        
        if challenge_allowed_membership_type.filter(membership_type=user_membership_type).exists:
            context={
                'object':week,
                'user_days':user_days
            }

        return render(request,"courses/week_detail.html",context)