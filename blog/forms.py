# blog/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django_ckeditor_5.widgets import CKEditor5Widget
from .models import Post


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditor5Widget(config_name="default"))  # CKEditor 5 for content

    class Meta:
        model = Post
        fields = ["title", "author", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Post"))
