import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, query):
    """Highlight query terms inside text with neon effect."""
    if not query:
        return text

    # Escape regex special characters
    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(
        lambda m: f'<span class="neon-highlight">{m.group(0)}</span>', 
        text
    )
    return mark_safe(highlighted)
