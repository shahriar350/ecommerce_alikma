from django.shortcuts import redirect
from django.urls import reverse_lazy
from rest_framework.response import Response


class CustomAdminPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/api/v1/' in request.path:
            if not request.user.is_authenticated and not request.user.is_superuser:
                return Response(status=401)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
