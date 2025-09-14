import json
import calendar
from datetime import date
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count, Q
from api.models import Article
from accounts.models import CustomUser
from comments.models import Comment
from .models import DashboardPreference
from django.views.decorators.http import require_POST



@login_required
def dashboard_home(request):
    """Main dashboard page with summary stats, recent articles, and charts."""
    # ----- Stats -----
    total_articles = Article.objects.count()
    total_users = CustomUser.objects.count()
    new_comments = Comment.objects.filter(created_at__date=timezone.now().date()).count()
    notifications = 5  # TODO: Replace with actual notifications logic

    # ----- Recent Articles -----
    recent_articles = Article.objects.order_by('-created_at')[:5]

    # ----- Monthly Articles Chart -----
    current_year = timezone.now().year
    monthly_counts = (
        Article.objects.filter(created_at__year=current_year)
        .extra(select={'month': "strftime('%%m', created_at)"})  # SQLite specific
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    monthly_labels = [calendar.month_name[i] for i in range(1, 13)]
    monthly_data = [0] * 12
    for m in monthly_counts:
        month_index = int(m['month']) - 1
        monthly_data[month_index] = m['count']

    # ----- Top Users -----
    top_users = (
        Article.objects.values("author__username")
        .annotate(article_count=Count("id"))
        .order_by("-article_count")[:5]
    )
    user_labels = [u["author__username"] for u in top_users]
    user_data = [u["article_count"] for u in top_users]

    # ----- Preferences -----
    prefs, _ = DashboardPreference.objects.get_or_create(user=request.user)

    context = {
        'total_articles': total_articles,
        'total_users': total_users,
        'new_comments': new_comments,
        'notifications': notifications,
        'recent_articles': recent_articles,
        'monthly_labels': monthly_labels,
        'monthly_data': monthly_data,
        'user_labels': user_labels,
        'user_data': user_data,
        'prefs': prefs,
    }
    return render(request, 'dashboard/dashboard_home.html', context)


def index(request):
    return HttpResponse("Welcome to the Dashboard!")


def get_chart_data(chart_type, cumulative, time_range, custom_start=None, custom_end=None):
    """Generate chart.js-ready data based on preferences."""
    qs = Article.objects.all()

    # ----- Date Filtering -----
    today = date.today()
    if time_range == "month":
        qs = qs.filter(created_at__year=today.year, created_at__month=today.month)
    elif time_range == "year":
        qs = qs.filter(created_at__year=today.year)
    elif time_range == "custom" and custom_start and custom_end:
        qs = qs.filter(created_at__date__range=[custom_start, custom_end])

    # ----- Aggregation -----
    users = (
        qs.values("author__username")
        .annotate(
            blog_count=Count("id", filter=Q(source="blog")),
            api_count=Count("id", filter=Q(source="api")),
        )
        .order_by("-blog_count", "-api_count")[:10]
    )

    labels = [u["author__username"] for u in users]
    blog_counts = [u["blog_count"] for u in users]
    api_counts = [u["api_count"] for u in users]

    data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Blog Articles",
                "data": blog_counts,
                "backgroundColor": "rgba(75, 192, 192, 0.6)",
            },
            {
                "label": "API Articles",
                "data": api_counts,
                "backgroundColor": "rgba(255, 99, 132, 0.6)",
            },
        ],
    }
    return data


@login_required
def update_preferences(request):
    """AJAX endpoint to update user preferences and return fresh chart data."""
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    prefs, _ = DashboardPreference.objects.get_or_create(user=request.user)
    data = json.loads(request.body.decode("utf-8"))

    prefs.chart_type = data.get("chart_type", prefs.chart_type)
    prefs.cumulative = data.get("cumulative", prefs.cumulative)
    prefs.time_range = data.get("time_range", prefs.time_range)

    # Safely assign custom dates
    prefs.custom_start = data.get("custom_start") or None
    prefs.custom_end = data.get("custom_end") or None
    prefs.save()

    chart_data = get_chart_data(
        prefs.chart_type,
        prefs.cumulative,
        prefs.time_range,
        prefs.custom_start,
        prefs.custom_end,
    )

    return JsonResponse({
        "chart_data": chart_data,
        "prefs": {
            "chart_type": prefs.chart_type,
            "cumulative": prefs.cumulative,
            "time_range": prefs.time_range,
            "custom_start": str(prefs.custom_start) if prefs.custom_start else None,
            "custom_end": str(prefs.custom_end) if prefs.custom_end else None,
        }
    })


@login_required
@require_POST
def save_preference(request):
    pref, _ = DashboardPreference.objects.get_or_create(user=request.user)
    key = request.POST.get("key")
    value = request.POST.get("value")

    if key == "chart_type" and value in dict(DashboardPreference.CHART_TYPES):
        pref.chart_type = value

    elif key == "cumulative":
        pref.cumulative = (value == "true")

    elif key == "time_range" and value in dict(DashboardPreference.TIME_RANGES):
        pref.time_range = value

    elif key == "custom_start":
        pref.custom_start = value or None

    elif key == "custom_end":
        pref.custom_end = value or None

    else:
        return JsonResponse({"success": False, "error": "Invalid key/value"})

    pref.save()
    return JsonResponse({"success": True, "key": key, "value": value})
