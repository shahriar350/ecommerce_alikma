from django.shortcuts import redirect
from django.urls import reverse_lazy


class CustomAdminPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if '/my/admin/' in request.path:
            if not request.user.is_authenticated and not request.user.is_superuser:
                return redirect(reverse_lazy('admin.login'))
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
