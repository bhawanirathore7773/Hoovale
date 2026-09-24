from django.http import HttpResponsePermanentRedirect


class CanonicalHostMiddleware:
    """Redirect the www hostname to HOOVALE's canonical non-www host."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        host = request.get_host().split(":", 1)[0].lower()
        if host == "www.hoovale.com":
            return HttpResponsePermanentRedirect(
                "https://hoovale.com" + request.get_full_path()
            )
        return self.get_response(request)
