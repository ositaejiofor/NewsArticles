from django import template

register = template.Library()

# --------------------------
# Sort Comments
# --------------------------
@register.filter
def sort_comments(comments, order=None):
    """
    Sort comments or replies by created_at.
    Defaults to 'latest' if no order is given.
    Usage:
      {{ comments|sort_comments }}        → latest first
      {{ comments|sort_comments:"oldest"}} → oldest first
    """
    if order == "oldest":
        return comments.order_by("created_at") if hasattr(comments, "order_by") else sorted(comments, key=lambda c: c.created_at)
    # default → latest
    return comments.order_by("-created_at") if hasattr(comments, "order_by") else sorted(comments, key=lambda c: c.created_at, reverse=True)


# --------------------------
# Get approved children
# --------------------------
@register.filter
def children(comment):
    """Return approved replies for a comment."""
    return comment.replies.filter(status="approved").order_by("created_at")


# --------------------------
# Get comment depth
# --------------------------
@register.filter
def get_depth(comment):
    """Return nesting depth of a comment (0 for top-level)."""
    depth = 0
    parent = getattr(comment, "parent", None)
    while parent:
        depth += 1
        parent = getattr(parent, "parent", None)
    return depth
