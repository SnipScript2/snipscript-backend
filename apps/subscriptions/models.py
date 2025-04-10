from django.db import models
from django.conf import settings
import os

User = settings.AUTH_USER_MODEL

class Feature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Features"
        ordering = ['name']


PACKAGE_TYPE = (
    ('month', 'MONTH'),
    ('year', 'YEAR'),
    ('week', 'WEEK'),
    ('day', 'DAY'),
    ('one-time', 'ONE-TIME'),
)

class Package(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    features = models.ManyToManyField(Feature)
    package_type = models.CharField(choices=PACKAGE_TYPE, default='month', max_length=255)
    conversation_limit = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    order = models.IntegerField(blank=True, null=True)

    stripe_product_id = models.CharField(max_length=255, blank=True)
    stripe_price_id = models.CharField(max_length=255, blank=True)  # ✅ Live mode
    stripe_price_id_test = models.CharField(max_length=255, blank=True)  # ✅ Test mode

    status = models.BooleanField(default=True)

    @property
    def total_price(self):
        if self.discount > 0:
            return self.price - (self.price * self.discount / 100)
        return self.price

    def get_stripe_price_id(self):
        """Returns the correct Stripe price ID based on STRIPE_MODE."""
        stripe_mode = os.getenv("STRIPE_MODE", "test").lower()
        return self.stripe_price_id if stripe_mode == "live" else self.stripe_price_id_test

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Packages"


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    conversation_left = models.IntegerField(null=True, blank=True)
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.package.name}'

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def save(self, *args, **kwargs):
        if self.status:
            self.conversation_left = self.package.conversation_limit
        super().save(*args, **kwargs)


class PromotionCode(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.PositiveIntegerField(help_text="Enter discount percentage (0-100)")
    duration = models.CharField(max_length=20, default="once")
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)
    stripe_promotion_code_id = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
