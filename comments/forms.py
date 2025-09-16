# comments/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Article, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))  # CKEditor 5

    class Meta:
        model = Article
        fields = ["title", "content", "author"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Post"))


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=CKEditor5Widget(config_name="default")  # CKEditor 5 for comments
    )
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.HiddenInput  # Hidden input for replies
    )

    class Meta:
        model = Comment
        fields = ["content", "parent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Post Comment"))
