from rest_framework import serializers
from .models import Package, Subscription


class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
        depth = 1

class SubscriptionSerializer(serializers.ModelSerializer):
    package = serializers.StringRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Subscription
        fields = '__all__'