from django.shortcuts import redirect
from django.urls import reverse


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # if not request.user.is_authenticated and not request.path_info.startswith(
        #         '/admin/') and not request.path_info.startswith('/pages/maintenance/'):
        #     return redirect(reverse('pages_maintenance'))

        if not request.user.is_authenticated and not request.path_info.startswith('/admin/'):
            return redirect('/admin/')

        response = self.get_response(request)
        return response
