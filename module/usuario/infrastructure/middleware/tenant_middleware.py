import threading
from django.utils.deprecation import MiddlewareMixin

_thread_local = threading.local()


def get_tenant_id() -> int | None:
    return getattr(_thread_local, "tenant_id", None)


def set_tenant_id(tenant_id: int | None) -> None:
    _thread_local.tenant_id = tenant_id


class TenantMiddleware(MiddlewareMixin):
    def process_request(self, request):
        tenant_id = self._extraer_tenant_id(request)
        set_tenant_id(tenant_id)
        request.tenant_id = tenant_id

    def process_response(self, request, response):
        set_tenant_id(None)
        return response

    def _extraer_tenant_id(self, request) -> int | None:
        if hasattr(request, "user") and request.user.is_authenticated:
            return getattr(request.user, "empresa_id", None)

        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if auth_header.startswith("Bearer "):
            return self._extraer_de_token(auth_header[7:])

        return None

    def _extraer_de_token(self, raw_token: str) -> int | None:
        try:
            from rest_framework_simplejwt.tokens import AccessToken
            token = AccessToken(raw_token)
            return token.get("empresa_id")
        except Exception:
            return None