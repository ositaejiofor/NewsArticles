from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Article, Category


# ------------------------
# Custom Form for Article
# ------------------------
class ArticleAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Article
        fields = "__all__"


# ------------------------
# Category Admin
# ------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# ------------------------
# Article Admin
# ------------------------
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm  # <-- attach custom form
    list_display = ("title", "author", "category", "created_at", "updated_at")
    list_filter = ("author", "category", "created_at", "updated_at")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    list_per_page = 20
