from rest_framework import serializers
from .models import Ad

class AdSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.username", read_only=True)

    class Meta:
        model = Ad
        fields = ["id", "title", "description", "image", "link", "owner", "owner_name", "created_at", "updated_at"]
        read_only_fields = ["id", "owner_name", "created_at", "updated_at"]
