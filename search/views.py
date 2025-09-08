from django.shortcuts import render
from django.db.models import Q
from blog.models import Article

def search_results(request):
    query = request.GET.get("q", "")
    results = []

    if query:
        results = Article.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__username__icontains=query) |
            Q(category__name__icontains=query)
        ).distinct()

    context = {
        "query": query,
        "results": results,
    }
    return render(request, "search/results.html", context)
