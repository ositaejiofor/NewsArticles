from django import template
import re



register = template.Library()

@register.simple_tag
def querystring(request, **kwargs):
    """
    Keeps existing query params and updates with new ones.
    Example usage: {% querystring request page=2 %}
    """
    query = request.GET.copy()
    for key, value in kwargs.items():
        query[key] = value
    return query.urlencode()


@register.filter
def highlight(text, search):
    """
    Highlight all occurrences of 'search' in the given text.
    """
    if not search:
        return text
    pattern = re.compile(re.escape(search), re.IGNORECASE)
    highlighted = pattern.sub(lambda m: f"<mark>{m.group(0)}</mark>", text)
    return highlighted

