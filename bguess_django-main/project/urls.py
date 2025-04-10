from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),                     # ✅ Admin is here
    path('sentry-debug/', trigger_error),
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.imgtocode.urls')),
    path('api/', include('apps.subscriptions.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# ✅ Auto-create superuser after migration (Render-friendly)
@receiver(post_migrate)
def create_default_admin(sender, **kwargs):
    User = get_user_model()
    if not User.objects.filter(email='admin@admin.com').exists():
        User.objects.create_superuser(
            email='admin@admin.com',
            password='123456'
        )
