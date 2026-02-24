from .models import AuditLog

class AuditMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.path.startswith('/admin') or request.path.startswith('/static'):
            return response

        user = request.user if request.user.is_authenticated else None

        ip = request.META.get('REMOTE_ADDR')

        AuditLog.objects.create(
            user=user,
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            ip_address=ip
        )

        return response
