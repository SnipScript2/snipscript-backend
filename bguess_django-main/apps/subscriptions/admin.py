from django.contrib import admin
from django import forms
from unfold.admin import ModelAdmin
from .models import Feature, Package, Subscription, PromotionCode


class PackageAdminForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        package_type = cleaned_data.get('package_type')

        if package_type == 'one-time':
            cleaned_data['is_recurring'] = False
        elif 'is_recurring' not in cleaned_data or cleaned_data['is_recurring'] is None:
            cleaned_data['is_recurring'] = True

        return cleaned_data


@admin.register(Package)
class PackageAdmin(ModelAdmin):
    form = PackageAdminForm
    list_display = ['name', 'price', 'discount', 'total_price', 'package_type', 'order']

    def save_model(self, request, obj, form, change):
        # Enforce is_recurring logic on save no matter what
        if obj.package_type == 'one-time':
            obj.is_recurring = False
        elif obj.is_recurring is None:
            obj.is_recurring = True
        super().save_model(request, obj, form, change)


@admin.register(Feature)
class FeatureAdmin(ModelAdmin):
    list_display = ['name']


@admin.register(Subscription)
class SubscriptionAdmin(ModelAdmin):
    list_display = ['user', 'package', 'start_date', 'status', 'end_date']


@admin.register(PromotionCode)
class PromotionCodeAdmin(ModelAdmin):
    list_display = ['name', 'code', 'discount_percent']
