from django.contrib import admin
from django import forms
from .models import Comment
from django_ckeditor_5.widgets import CKEditor5Widget


# Custom form for Comment model to use CKEditor5
class CommentAdminForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = "__all__"
        widgets = {
            "content": CKEditor5Widget(config_name="default"),
        }


class ReplyInline(admin.StackedInline):
    model = Comment
    fk_name = "parent"  # Make sure Comment has a 'parent' FK to itself
    extra = 0
    fields = ("user", "content", "created_at")
    readonly_fields = ("created_at",)
    can_delete = True
    show_change_link = True


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    form = CommentAdminForm  # attach CKEditor5 form here
    list_display = ("id", "article", "user", "indented_content", "created_at")
    list_filter = ("created_at", "article")
    search_fields = ("user__username", "content", "article__title")
    ordering = ("-created_at",)
    list_per_page = 20
    inlines = [ReplyInline]

    def indented_content(self, obj):
        """Show replies indented under parent comments in list view."""
        indent = "— " * self.get_depth(obj)
        text = f"{indent}{obj.content[:50]}"  # show first 50 chars for brevity
        if len(obj.content) > 50:
            text += "..."
        return text

    indented_content.short_description = "Comment"

    def get_depth(self, obj):
        """Recursively calculate depth of a comment based on parent."""
        depth = 0
        parent = obj.parent
        while parent:
            depth += 1
            parent = parent.parent
        return depth
