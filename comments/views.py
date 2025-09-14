from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseBadRequest


from .models import Comment
from .forms import CommentForm
from blog.models import Article


# -------------------------------------------------------------------
# Public Article Detail
# -------------------------------------------------------------------

def article_detail(request, slug):
    """
    Display an article with approved top-level comments and a form.
    """
    article = get_object_or_404(Article, slug=slug)
    comments = (
        article.comments.filter(parent__isnull=True, status="approved")
        .select_related("user")
        .prefetch_related("children", "likes")
        .order_by("-created_at")
    )
    form = CommentForm()
    return render(
        request,
        "blog/article_detail.html",
        {"article": article, "comments": comments, "form": form},
    )


@login_required
def comments_home(request):
    """
    Show all comments globally (for testing / browsing).
    """
    comments = Comment.objects.select_related("article", "user").order_by("-created_at")
    return render(request, "comments/comments_home.html", {"comments": comments})


# -------------------------------------------------------------------
# Comment CRUD (AJAX-friendly)
# -------------------------------------------------------------------

@login_required
@require_POST
def add_comment(request):
    """
    Add a top-level comment (AJAX or fallback POST).
    """
    form = CommentForm(request.POST)
    article = get_object_or_404(Article, id=request.POST.get("article_id"))

    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()

        # If AJAX -> return partial HTML
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            html = render_to_string(
                "blog/_comment.html",
                {"comment": comment, "reply_form": CommentForm(), "request": request},
            )
            return JsonResponse({"success": True, "html": html})

        # Normal form fallback
        return redirect("blog:article_detail", slug=article.slug)

    return JsonResponse({"success": False, "error": form.errors}, status=400)


@login_required
def reply_comment(request, comment_id):
    if request.method == "POST":
        parent = get_object_or_404(Comment, id=comment_id)
        content = request.POST.get("content", "").strip()

        if not content:
            return JsonResponse({"success": False, "error": "Content is required."}, status=400)

        # Create reply
        reply = Comment.objects.create(
            article=parent.article,
            user=request.user,
            content=content,
            parent=parent
        )

        # Render only the reply HTML
        html = render_to_string(
            "blog/_comment.html",
            {"comment": reply, "reply_form": CommentForm()},
            request=request
        )

        return JsonResponse({
            "success": True,
            "parent_id": parent.id,
            "html": html
        })

    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)


@login_required
@require_POST
def edit_comment(request):
    """
    Edit own comment (AJAX only).
    """
    comment = get_object_or_404(
        Comment, id=request.POST.get("comment_id"), user=request.user
    )
    content = request.POST.get("content", "").strip()

    if not content:
        return JsonResponse({"success": False, "error": "Content required"}, status=400)

    comment.content = content
    comment.save()

    html = render_to_string(
        "blog/_comment.html",
        {"comment": comment, "reply_form": CommentForm(), "request": request},
    )
    return JsonResponse({"success": True, "comment_id": comment.id, "html": html})


@login_required
@require_POST
def toggle_like(request):
    """
    Like or unlike a comment (AJAX only).
    """
    comment = get_object_or_404(Comment, id=request.POST.get("comment_id"))
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)
        liked = False
    else:
        comment.likes.add(user)
        liked = True

    return JsonResponse(
        {
            "success": True,
            "comment_id": comment.id,
            "liked": liked,
            "likes_count": comment.likes.count(),
        }
    )


# -------------------------------------------------------------------
# Notifications
# -------------------------------------------------------------------

@login_required
def check_notifications(request):
    """
    Return unseen replies for the current user and mark them as notified.
    """
    new_replies = (
        Comment.objects.filter(parent__user=request.user, notified=False, status="approved")
        .select_related("article", "user")
        .order_by("-created_at")
    )

    new_replies.update(notified=True)

    data = [
        {
            "id": c.id,
            "content": c.content,
            "article_id": c.article.id,
            "article_title": c.article.title,
            "replier": c.user.username,
            "created_at": c.created_at.strftime("%b %d, %Y %H:%M"),
        }
        for c in new_replies
    ]

    return JsonResponse({"success": True, "notifications": data})


# -------------------------------------------------------------------
# Staff Moderation
# -------------------------------------------------------------------

@staff_member_required
def pending_comments(request):
    """
    View all pending comments for staff review.
    """
    comments = Comment.objects.filter(status="pending").order_by("-created_at")
    return render(request, "comments/pending_comments.html", {"comments": comments})


@staff_member_required
@require_POST
def update_comment_status(request):
    """
    Approve or reject a pending comment.
    """
    comment = get_object_or_404(Comment, id=request.POST.get("comment_id"))
    action = request.POST.get("action")

    if action not in ["approve", "reject"]:
        return JsonResponse({"success": False, "error": "Invalid action"}, status=400)

    comment.status = "approved" if action == "approve" else "rejected"
    comment.save()

    return JsonResponse({"success": True})
