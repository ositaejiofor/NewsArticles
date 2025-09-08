from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Article, Category
from comments.forms import CommentForm


def home(request):
    """Homepage showing a paginated list of posts with sidebar data + search."""
    query = request.GET.get("q")  # search query
    posts = Article.objects.all().order_by('-created_at')

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    # Pagination
    paginator = Paginator(posts, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Sidebar data
    recent_posts = Article.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'categories': categories,
        'query': query,  # keep query in context
    }
    return render(request, 'blog/home.html', context)


def posts_by_category(request, slug):
    """Show posts filtered by category slug."""
    category = get_object_or_404(Category, slug=slug)
    posts = Article.objects.filter(category=category).order_by('-created_at')

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'blog/home.html', context)


def post_detail(request, slug):
    """Detail page for a single post with comments + sidebar data."""
    post = get_object_or_404(Article, slug=slug)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user  # assign logged-in user
            comment.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = CommentForm()

    # Sidebar data
    recent_posts = Article.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'recent_posts': recent_posts,
        'categories': categories,
    }
    return render(request, 'blog/post_detail.html', context)


def posts_by_category(request, slug):
    """Show posts filtered by category slug."""
    category = get_object_or_404(Category, slug=slug)
    posts = Article.objects.filter(category=category).order_by('-created_at')

    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()

    paginator = Paginator(posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recent_posts = Article.objects.order_by('-created_at')[:5]
    categories = Category.objects.all()

    context = {
        'page_obj': page_obj,
        'recent_posts': recent_posts,
        'categories': categories,
        'selected_category': category,
        'query': query,   # ✅ keep query in context for highlighting
    }
    return render(request, 'blog/home.html', context)
