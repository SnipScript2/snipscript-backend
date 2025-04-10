from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Package, PromotionCode, Subscription
import stripe
import logging

logger = logging.getLogger(__name__)
stripe.api_key = settings.STRIPE_SECRET_KEY

@receiver(post_save, sender=Package)
def sync_stripe_package(sender, instance, created, **kwargs):
    try:
        update_fields = []
        if not instance.stripe_product_id:
            product = stripe.Product.create(
                name=instance.name,
                description=instance.description or ""
            )
            instance.stripe_product_id = product.id
            update_fields.append("stripe_product_id")

        if instance.stripe_price_id:
            stripe.Price.modify(instance.stripe_price_id, active=False)

        price_args = {
            "product": instance.stripe_product_id,
            "unit_amount": int(instance.total_price * 100),
            "currency": "usd",
        }

        if instance.package_type in ["day", "week", "month", "year"]:
            price_args["recurring"] = {"interval": instance.package_type}

        new_price = stripe.Price.create(**price_args)
        instance.stripe_price_id = new_price.id
        update_fields.append("stripe_price_id")

        if update_fields:
            Package.objects.filter(pk=instance.pk).update(**{f: getattr(instance, f) for f in update_fields})

    except Exception as e:
        logger.error("Stripe sync error for Package ID %s: %s", instance.id, str(e))


from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

@receiver(post_save, sender=User)
def create_subscription_for_new_user(sender, instance, created, **kwargs):
    if created:
        try:
            default_package = Package.objects.get(name="Free")
        except Package.DoesNotExist:
            default_package = Package.objects.first()

        Subscription.objects.create(
            user=instance,
            package=default_package,
            status=True,
            start_date=datetime.now(),
            conversation_left=default_package.conversation_limit,
        )

