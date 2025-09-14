from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Article
from blog.models import Category



def home(request):
    # Latest articles (most recent 6)
    latest_articles = Article.objects.all().order_by('-created_at')[:6]

    # Popular articles (placeholder: first 5 articles)
    popular_articles = Article.objects.all().order_by('id')[:5]

    # Featured articles (top 4 latest as placeholder)
    featured_articles = Article.objects.all().order_by('-created_at')[:4]

    # Categories
    categories = Category.objects.all() if 'Category' in globals() else []

    context = {
        "latest_articles": latest_articles,
        "popular_articles": popular_articles,
        "featured_articles": featured_articles,
        "categories": categories,
    }
    return render(request, "home.html", context)

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def privacy_policy(request):
    return render(request, "core/privacy_policy.html")

def terms_of_service(request):
    return render(request, "core/terms_of_service.html")

def disclaimer(request):
    return render(request, "core/disclaimer.html")