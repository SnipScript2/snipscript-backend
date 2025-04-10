# from rest_framework import serializers
# from .models import DesignRequest
# class DesignRequestSerializer(serializers.Serializer):
#     image = serializers.ImageField(required=False)
#     prompt = serializers.CharField(required=True)


# class DesignHistorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DesignRequest
#         fields = ["id", "prompt", "image", "ai_response", "created_at"]



from rest_framework import serializers
from .models import DesignRequest

class DesignRequestSerializer(serializers.Serializer):
    image = serializers.ImageField(required=False)
    url = serializers.URLField(required=False)  # New field for URL
    prompt = serializers.CharField(required=True)

class DesignHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignRequest
        fields = ["id", "prompt", "url", "image", "ai_response", "created_at"]