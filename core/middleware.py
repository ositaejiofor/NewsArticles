import logging
from django.shortcuts import redirect
from django.conf import settings

logger = logging.getLogger(__name__)

class RedirectSchemeMiddleware:
    """
    Fixes incorrect scheme issues:
    - In development: redirects HTTPS → HTTP (devserver only supports HTTP).
    - In production: redirects HTTP → HTTPS (force secure connections).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        scheme = request.META.get("wsgi.url_scheme")

        # Development mode: HTTPS → HTTP
        if settings.RENDER_ENV != "production" and scheme == "https":
            http_url = request.build_absolute_uri().replace("https://", "http://", 1)
            logger.warning(f"[RedirectSchemeMiddleware] Dev mode: HTTPS → HTTP {http_url}")
            return redirect(http_url)

        # Production mode: HTTP → HTTPS
        if settings.RENDER_ENV == "production" and scheme == "http":
            https_url = request.build_absolute_uri().replace("http://", "https://", 1)
            logger.warning(f"[RedirectSchemeMiddleware] Prod mode: HTTP → HTTPS {https_url}")
            return redirect(https_url)

        return self.get_response(request)
