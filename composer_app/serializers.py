from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Article
        fields = ["id", "title", "slug", "content", "author", "author_name", "created_at", "updated_at"]
        read_only_fields = ["id", "author_name", "created_at", "updated_at"]
