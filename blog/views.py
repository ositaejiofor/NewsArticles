from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Article, Category
from comments.forms import CommentForm

def home(request):
    """Homepage showing a paginated list of articles with search and sidebar."""
    query = request.GET.get("q")
    articles = Article.objects.all().order_by("-created_at")

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by("-created_at")[:5]
    categories = Category.objects.all()

    context = {
        "page_obj": page_obj,
        "recent_posts": recent_posts,
        "categories": categories,
        "query": query,
    }
    return render(request, "blog/home.html", context)


def posts_by_category(request, slug):
    """Show articles filtered by category."""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by("-created_at")

    query = request.GET.get("q")
    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by("-created_at")[:5]
    categories = Category.objects.all()

    context = {
        "page_obj": page_obj,
        "recent_posts": recent_posts,
        "categories": categories,
        "selected_category": category,
        "query": query,
    }
    return render(request, "blog/home.html", context)


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            return redirect("blog:article_detail", slug=article.slug)
    else:
        form = CommentForm()

    # Fetch only top-level comments, replies will be accessed via .replies.all
    comments = article.comments.filter(parent__isnull=True).order_by("created_at")

    return render(request, "blog/article_detail.html", {
        "article": article,
        "comments": comments,
        "form": form,
    })


def category_detail(request, slug):
    """Category detail page listing all articles in the category."""
    category = get_object_or_404(Category, slug=slug)
    articles = Article.objects.filter(category=category).order_by("-created_at")

    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by("-created_at")[:5]
    categories = Category.objects.all()

    context = {
        "category": category,
        "page_obj": page_obj,
        "articles": articles,
        "recent_posts": recent_posts,
        "categories": categories,
    }
    return render(request, "blog/category_detail.html", context)


def article_list(request):
    """Simple list of all articles."""
    articles = Article.objects.all().order_by("-created_at")
    paginator = Paginator(articles, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by("-created_at")[:5]
    categories = Category.objects.all()

    context = {
        "articles": articles,
        "page_obj": page_obj,
        "recent_posts": recent_posts,
        "categories": categories,
    }
    return render(request, "blog/article_list.html", context)


def article_list(request):
    """List all articles with pagination."""
    article_qs = Article.objects.all().order_by("-created_at")

    # Paginate (6 per page, adjust as needed)
    paginator = Paginator(article_qs, 6)
    page_number = request.GET.get("page")
    articles = paginator.get_page(page_number)

    return render(request, "blog/article_list.html", {"articles": articles})