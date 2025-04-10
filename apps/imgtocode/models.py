from django.db import models
from apps.users.models import User
import cloudinary
import cloudinary.models

class DesignRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="design_requests")
    prompt = models.TextField()
    prompt_hash = models.CharField(max_length=64, null=True, blank=True)  # ✅ Allow nulls to avoid DB crash
    url = models.URLField(blank=True, null=True)
    image = cloudinary.models.CloudinaryField('image', blank=True, null=True)
    ai_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.email} on {self.created_at}"
