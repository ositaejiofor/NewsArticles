from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm



# Registration form
class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

# Login form
class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"autofocus": True, "class": "form-control"})
    )

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        # Exclude the current user from uniqueness check
        if User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        # Optional: make sure email is unique
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
    

class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "New Password"})
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add Bootstrap classes & placeholders
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                "class": "form-control",
                "placeholder": field.label
            })

        # Special handling for password & profile_image
        self.fields["profile_image"].widget.attrs.update({
            "class": "form-control"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control"
        })
