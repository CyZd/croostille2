from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path

from .views import MembershipSelectView,PaymentView,updateTransactions,profile_view,cancelSubscription,UserCreateProfile

app_name='memberships'

urlpatterns = [
    path('', MembershipSelectView.as_view(),name='offres'),
    path('paiement/', PaymentView,name='paiement'),
    path('update-transactions/<subscription_id>', updateTransactions,name='update-transactions'),
    path('profile/', profile_view,name='profil'),
    path('createProfile/', UserCreateProfile.as_view(),name='creer_profil'),
    path('cancel/', cancelSubscription,name='annuler'),
]

