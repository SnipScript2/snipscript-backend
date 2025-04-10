from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.response import Response

from apps.subscriptions.models import Package, Subscription
from .models import User

import logging
import stripe
from django.conf import settings

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=User)
def create_free_subscription(sender,instance, created, **kwargs):
    if created:
        try:
            free_package = Package.objects.filter(price=0,status=True).first()
            if not free_package:
                logger.warning("No free package found for user: %s", instance.email)
                return
            
            Subscription.objects.create(
                user=instance,
                package=free_package,
                status=True
            )
            logger.info("Free subscription created for user: %s", instance.email)

        except stripe.error.StripeError as e:
            logger.error("Stripe error for user %s: %s", instance.email, str(e))


