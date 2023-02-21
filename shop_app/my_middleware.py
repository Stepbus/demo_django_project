from django.core.cache import cache


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        cache.set(str(request.user), 'Online', 120)
        response = self.get_response(request)

        return response
