from django.shortcuts import render

from django.views.generic import ListView, DetailView,View
from .models import Challenge, Week

from memberships.models import UserMembership


class CourseListView(ListView):
    model=Challenge

class CourseDetailView(DetailView):
    model=Challenge

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
        
        if challenge_allowed_membership_type.filter(membership_type=user_membership_type).exists:
            context={
                'object':week
            }

        return render(request,"courses/week_detail.html",context)