from django.contrib.sitemaps import Sitemap
from .models import Article, Category
from accounts.models import CustomUser


class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        # Use updated_at if you have it, else created_at
        if hasattr(obj, "updated_at"):
            return obj.updated_at
        return None

    def location(self, obj):
        return obj.get_absolute_url()


class UserSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return CustomUser.objects.all()

    def lastmod(self, obj):
        # Using date_joined as last modification date
        return obj.date_joined

    def location(self, obj):
        if hasattr(obj, "get_absolute_url"):
            return obj.get_absolute_url()
        # fallback if no get_absolute_url
        return f"/accounts/profile/{obj.username}/"
