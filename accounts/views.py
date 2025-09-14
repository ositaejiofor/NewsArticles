from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomRegisterForm, CustomLoginForm, ProfileUpdateForm
from api.models import Article
from comments.models import Comment
from django.utils.timezone import now
from django.db.models import Count
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.contrib.auth import logout
from django.contrib.auth import login






# ------------------------
# Dashboard / Profile Overview
# ------------------------
@login_required
def dashboard(request):
    """Show user dashboard with recent articles, comments, and logins."""
    user = request.user

    # Fetch recent activity
    recent_articles = Article.objects.filter(author=user).order_by('-created_at')[:5]
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:5]
    recent_logins = [{"timestamp": user.last_login, "ip": "127.0.0.1"}]  # Replace with real IP tracking

    context = {
        "recent_articles": recent_articles,
        "recent_comments": recent_comments,
        "recent_logins": recent_logins,
    }
    return render(request, "accounts/profile_dashboard.html", context)


# ------------------------
# Custom Login
# ------------------------
class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        return '/accounts/dashboard/'  # redirect to dashboard


# ------------------------
# Registration
# ------------------------
def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("accounts:dashboard")
    else:
        form = CustomRegisterForm()
    return render(request, "accounts/register.html", {"form": form})


# ------------------------
# Profile View
# ------------------------
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


# ------------------------
# Edit Profile
# ------------------------
@login_required
def edit_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)

            # Handle password change
            new_password = form.cleaned_data.get("password")
            if new_password:
                user.set_password(new_password)

            user.save()
            messages.success(request, "Your profile has been updated successfully!")
            return redirect("accounts:edit_profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/edit_profile.html", {"form": form})


# ------------------------
# Logout
# ------------------------
def logout_view(request):
    logout(request)
    return redirect('core:home')

def profile(request):
    return render(request, "accounts/profile.html")


@login_required
def profile_dashboard(request):
    user = request.user

    # Example recent activity
    recent_articles = Article.objects.filter(author=user).order_by('-created_at')[:5]
    recent_comments = Comment.objects.filter(user=user).order_by('-created_at')[:5]
    recent_logins = getattr(user, 'login_records', [])  # Replace with your login model/query if exists

    # Analytics: last 12 months
    last_12_months = [(now().replace(day=1) - relativedelta(months=i)) for i in range(11, -1, -1)]
    article_labels = [d.strftime("%b %Y") for d in last_12_months]
    article_data = [
        Article.objects.filter(author=user, created_at__year=d.year, created_at__month=d.month).count()
        for d in last_12_months
    ]
    comment_labels = article_labels
    comment_data = [
        Comment.objects.filter(user=user, created_at__year=d.year, created_at__month=d.month).count()
        for d in last_12_months
    ]

    context = {
        'recent_articles': recent_articles,
        'recent_comments': recent_comments,
        'recent_logins': recent_logins,
        'article_labels': article_labels,
        'article_data': article_data,
        'comment_labels': comment_labels,
        'comment_data': comment_data,
    }
    return render(request, "accounts/profile_dashboard.html", context)

@login_required
def profile_analytics_data(request):
    # Example: return dummy chart data
    article_labels = ["Jan", "Feb", "Mar"]
    article_data = [5, 8, 3]
    comment_labels = ["Jan", "Feb", "Mar"]
    comment_data = [10, 4, 7]

    return JsonResponse({
        "article_labels": article_labels,
        "article_data": article_data,
        "comment_labels": comment_labels,
        "comment_data": comment_data,
    })