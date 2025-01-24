from django.http import JsonResponse

class APIAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/v1/'):
            if not request.headers.get('X-CSRFToken'):
                return JsonResponse({'error': 'CSRF token missing'}, status=403)
        return self.get_response(request) 