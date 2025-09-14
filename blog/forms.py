# blog/forms.py
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from ckeditor.widgets import CKEditorWidget
from .models import Post

class PostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())  # use CKEditor for content

    class Meta:
        model = Post
        fields = ["title", "author", "content"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Save Post"))
