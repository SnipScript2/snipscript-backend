from django.urls import path 
from . import views 

urlpatterns = [
    path('packages/', views.PackageView.as_view()),
    path('checkout/<int:package_id>/', views.SubscriptionCreateView.as_view()),
    path('subscriptions/', views.SubscriptionView.as_view()),
    path('subscriptions/cancel/<int:subscription_id>/',views.CancelSubscriptionView.as_view()),
    path('webhook/', views.stripe_webhook, name='webhook'),


]