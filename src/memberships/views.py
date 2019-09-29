from django.shortcuts import render,redirect

from django.contrib import messages

from django.views.generic import ListView
from django.views import generic
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm

from django.conf import settings

from .models import Membership, UserMembership, Subscription
from django.contrib.auth.models import AnonymousUser,User

from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.urls import reverse
from django.urls import reverse_lazy

from django.http import HttpResponse, HttpResponseRedirect

import stripe

#import request

def userHomepage(request):
    return render(request,'memberships/homepage.html')

def userConnect(request):
    return render(request,'memberships/registration/login.html')

def userDisconnect(request):
    logout(request)
    return redirect('homepage')

def profile_view(request):
    user_membership=get_user_membership(request)
    user_subscription=get_user_subscription(request)
    context={
        'user_membership':user_membership,
        'user_subscription':user_subscription
    }
    return render(request,"memberships/profile.html", context)

def get_user_membership(request):
    user_membership_queryset=UserMembership.objects.filter(user=request.user)
    if user_membership_queryset.exists():
        return user_membership_queryset.first()
    return None

def get_user_subscription(request):
    user_subscription_queryset=Subscription.objects.filter(
        user_membership=get_user_membership(request)
    )
    if user_subscription_queryset.exists():
        user_subscription=user_subscription_queryset.first()
        return user_subscription
    return None

def get_selected_membership(request):
    membership_type=request.session['selected_membership_type']
    selected_membership_queryset=Membership.objects.filter(
            membership_type=request.POST.get('membership_type')
        )
    if selected_membership_queryset.exists():
        return selected_membership_queryset.first()
    return None

class UserCreateProfile(generic.CreateView):
    membership = request.session.get('membership')
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('creer_profil')
    template_name = 'memberships/registration/userCreateProfile.html'

class MembershipSelectView(ListView):
    model = Membership
    def anonymous_redirect(request):
        if request.user.is_anonymous:
            return HttpResponseRedirect('memberships/createProfile')

    def get_context_data(self, *args, **kwargs):
        if not AnonymousUser.is_anonymous:
            context=super().get_context_data(**kwargs)
            current_membership=get_user_membership(self.request)
            context['current_membership']=str(current_membership.membership)
            return context
        else:
            context=super().get_context_data(**kwargs)
            return context
    
    def post(self, request, **kwargs):
        if request.user.is_anonymous:
            membership_type=request.POST.get('membership_type')
            request.session['membership']=membership_type
            return HttpResponseRedirect('createProfile')
        else:
            selected_membership_type=request.POST.get('membership_type')

            user_membership=get_user_membership(request)
            user_subscription=get_user_subscription(request)

            selected_membership_queryset=Membership.objects.filter(
                membership_type=request.POST.get('membership_type')
            )
            if selected_membership_queryset.exists():
                selected_membership=selected_membership_queryset.first()

            if user_membership.membership==selected_membership:
                if user_subscription != None:
                    messages.info(request,"Vous êtes déjà abonné à cette formule")
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            
            request.session['selected_membership_type']=selected_membership.membership_type

            return HttpResponseRedirect(reverse('memberships:paiement'))

def PaymentView(request):
    user_membership=get_user_membership(request)
    selected_membership=get_selected_membership(request)

    publishKey=settings.STRIPE_PUBLISHABLE_KEY

    if request.method=="POST":
        try:
            token=request.POST['stripeToken']
            subscription= stripe.Subscription.create(
                customer=user_membership.stripe_customer_id,
                items=[
                    {
                        "plan": selected_membership.stripe_plan_id,
                    },
                ],
                default_source=token,
            )

            return redirect(reverse('memberships:update-transactions',
                kwargs={
                    'subscription_id': subscription.id
                }
            ))

        except stripe.error.CardError as e:
            messages.info(request,"Votre carte a été rejetée.")


    context={
        'publishKey':publishKey,
        'selected_membership':selected_membership
    }

    return render(request, 'memberships/membership_payment.html',context)

def updateTransactions(request, subscription_id):
    user_membership=get_user_membership(request)
    selected_membership=get_selected_membership(request)

    user_membership.membership=selected_membership
    user.membership.save()

    sub, created=Subscription.objects.get_or_create(user_membership=user_membership)
    sub.stripe_subscription_id=subscription_id
    sub.active=True 
    sub.save()

    try:
        del request.session['selected_membership_type']
    except:
        pass

    messages.info(request,"L'abonnement {} a bien été crée.".format(selected_membership))
    return redirect('/courses')

def cancelSubscription(request):
    user_subscription=get_user_subscription(request)

    if user.active==False:
        messages.info(request,"Vous n'avez pas d'abonnement en cours.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    sub=stripe.Subscription.retrieve(user_sub.stripe_subscription_id)
    sub.delete()

    user_subscription.active=False
    user_subscription.save()

    messages.info(request,"Votre abonnement a bien été annulé.")

    return HttpResponseRedirect('memberships/')


