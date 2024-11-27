from django.http import HttpResponseRedirect
from django.urls import reverse


class UnderDevelopmentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Exclude the under development page from redirection
        if request.path == reverse("under_development"):
            return self.get_response(request)

        # Redirect all other requests to the under development page
        response = HttpResponseRedirect(reverse("under_development"))
        return response
