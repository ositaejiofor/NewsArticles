from django.shortcuts import redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .models import Comment
from .forms import CommentForm
from django.shortcuts import render
from blog.models import Article  # adjust if needed
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from blog.models import Article



def comments_home(request):
    comments = Comment.objects.all().order_by('-created_at')
    return render(request, 'comments/home.html', {'comments': comments})



@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Article, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            parent_id = request.POST.get("parent_id")
            if parent_id:
                comment.parent_id = int(parent_id)
            comment.status = "approved"  # or "pending"
            comment.save()

            # SEND EMAIL NOTIFICATION IF THIS IS A REPLY
            if comment.parent:
                parent_user = comment.parent.user
                if parent_user.email and parent_user != request.user:
                    post_url = request.build_absolute_uri(reverse("post_detail", args=[post.id]))
                    send_mail(
                        subject=f"New reply to your comment on {post.title}",
                        message=f"Hi {parent_user.username},\n\n{request.user.username} replied to your comment:\n\n\"{comment.content}\"\n\nSee it here: {post_url}",
                        from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@yourdomain.com',
                        recipient_list=[parent_user.email],
                        fail_silently=True,
                    )

            return JsonResponse({
                "id": comment.id,
                "user": comment.user.username,
                "content": comment.content,
                "created_at": comment.created_at.strftime("%b %d, %Y %H:%M"),
                "parent_id": comment.parent_id or "",
                "like_count": comment.like_count()
            })

    return JsonResponse({"error": "Invalid request"}, status=400)



@staff_member_required
def pending_comments(request):
    comments = Comment.objects.filter(status="pending").order_by("-created_at")
    return render(request, "comments/pending_comments.html", {"comments": comments})


@staff_member_required
@csrf_exempt
def update_comment_status(request):
    if request.method == "POST":
        comment_id = request.POST.get("id")
        action = request.POST.get("action")
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            if action == "approve":
                comment.status = "approved"
            elif action == "reject":
                comment.status = "rejected"
            comment.save()
            return JsonResponse({"success": True})
    return JsonResponse({"success": False}, status=400)


@login_required
@csrf_exempt
def toggle_like(request):
    if request.method == "POST":
        comment_id = request.POST.get("id")
        comment = Comment.objects.filter(id=comment_id).first()
        if comment:
            if request.user in comment.likes.all():
                comment.likes.remove(request.user)
            else:
                comment.likes.add(request.user)
            return JsonResponse({"like_count": comment.like_count()})
    return JsonResponse({"error": "Invalid request"}, status=400)


def home(request):
    return render(request, "comments/home.html")