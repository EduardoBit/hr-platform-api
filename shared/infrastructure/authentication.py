from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class _UsuarioAutenticado:
    """Usuario mínimo que satisface IsAuthenticated sin usar auth.User de Django."""
    is_authenticated = True
    is_active = True

    def __init__(self, usuario_id, empresa_id, rol):
        self.pk = usuario_id
        self.id = usuario_id
        self.empresa_id = empresa_id
        self.rol = rol


class CustomJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth_header:
            return None

        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return None

        try:
            token = JWTAuthentication().get_validated_token(parts[1])
        except (InvalidToken, TokenError):
            raise AuthenticationFailed("Token inválido o expirado.")

        usuario_id = token.get("usuario_id")
        if usuario_id is None:
            raise AuthenticationFailed("Token no contiene identificación de usuario.")

        user = _UsuarioAutenticado(
            usuario_id=usuario_id,
            empresa_id=token.get("empresa_id"),
            rol=token.get("rol"),
        )
        return (user, token)

    def authenticate_header(self, request):
        return "Bearer"
