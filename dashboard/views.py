from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Count
from api.models import Article
from accounts.models import CustomUser
from comments.models import Comment
import calendar


@login_required
def dashboard_home(request):
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

    # Prepare labels and data for chart.js
    monthly_labels = [calendar.month_name[i] for i in range(1, 13)]
    monthly_data = [0] * 12
    for m in monthly_counts:
        month_index = int(m['month']) - 1
        monthly_data[month_index] = m['count']

    # ----- User Activity Chart -----
    top_users = CustomUser.objects.all()[:5]
    user_labels = [user.username for user in top_users]
    user_data = [user.articles.count() for user in top_users]  # requires related_name="articles"

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
    }

    return render(request, 'dashboard/dashboard_home.html', context)


def index(request):
    return HttpResponse("Welcome to the Dashboard!")
