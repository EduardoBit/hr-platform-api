from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JwtMiddleware(MiddlewareMixin):
    def process_request(self, request):
        authenticator = JWTAuthentication()
        try:
            result = authenticator.authenticate(request)
            if result is not None:
                user, token = result
                request.user = user
                request.auth = token
                request.empresa_id = token.get("empresa_id")
                request.rol = token.get("rol")
                request.usuario_id = token.get("usuario_id")
        except (InvalidToken, TokenError):
            pass