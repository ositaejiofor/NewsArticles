
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomRegisterForm
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from api.models import Article
from comments.models import Comment



class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    # Ensure login redirects to dashboard
    def get_success_url(self):
        return '/dashboard/'




@login_required
def dashboard(request):
    return render(request, "dashboard.html")


def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after registration
            return redirect("/dashboard/")
    else:
        form = CustomRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
def edit_profile(request):
    if request.method == "POST":
        user = request.user
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_image = request.FILES.get("profile_image")

        if full_name:
            names = full_name.split(" ", 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ""

        user.username = username
        user.email = email

        if password:
            user.set_password(password)

        if profile_image:
            user.profile_image = profile_image

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")

    return render(request, "accounts/edit_profile.html")


@login_required
def profile_dashboard(request):
    user = request.user

    # Handle profile edit
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        profile_image = request.FILES.get("profile_image")

        if full_name:
            names = full_name.split(" ", 1)
            user.first_name = names[0]
            user.last_name = names[1] if len(names) > 1 else ""

        user.username = username
        user.email = email

        if password:
            user.set_password(password)

        if profile_image:
            user.profile_image = profile_image

        user.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile_dashboard")

    # Recent activity
    recent_articles = Article.objects.filter(author=user).order_by('-created_at')[:5]
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:5]
    recent_logins = [{"timestamp": user.last_login, "ip": "127.0.0.1"}]

    context = {
        "recent_articles": recent_articles,
        "recent_comments": recent_comments,
        "recent_logins": recent_logins,
    }
    return render(request, "accounts/profile_dashboard.html", context)


def logout_view(request):
    logout(request)
    return redirect('core:home')