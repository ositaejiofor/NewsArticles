# comments/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget
from .models import Article, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # Rich text editor

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
        widget=CKEditorWidget(config_name="default")  # Rich text editor for comments
    )
    parent = forms.ModelChoiceField(
        queryset=Comment.objects.all(),
        required=False,
        widget=forms.HiddenInput  # Hidden input to track parent comment for replies
    )

    class Meta:
        model = Comment
        fields = ["content", "parent"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Post Comment"))
