from typing import Optional, List
from modules.usuario.domain.entities.rol import Rol
from modules.usuario.domain.repositories.rol_repository import RolRepository
from modules.usuario.infrastructure.models.rol_model import RolModel


class DjangoRolRepository(RolRepository):
    def get_by_id(self, id: int) -> Optional[Rol]:
        try:
            return self._to_entity(RolModel.objects.get(pk=id))
        except RolModel.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str, empresa_id: Optional[int] = None) -> Optional[Rol]:
        qs = RolModel.objects.filter(nombre=nombre)
        if empresa_id is not None:
            qs = qs.filter(empresa_id=empresa_id)
        else:
            qs = qs.filter(empresa_id__isnull=True)
        try:
            return self._to_entity(qs.first())
        except Exception:
            return None

    def get_by_empresa(self, empresa_id: int) -> List[Rol]:
        return [
            self._to_entity(m)
            for m in RolModel.objects.filter(empresa_id=empresa_id)
        ]

    def save(self, rol: Rol) -> Rol:
        if rol.id:
            model = RolModel.objects.get(pk=rol.id)
        else:
            model = RolModel()

        model.empresa_id = rol.empresa_id
        model.nombre = rol.nombre
        model.permisos = list(rol.permisos)
        model.es_sistema = rol.es_sistema
        model.save()

        rol.id = model.pk
        return rol

    def exists(self, id: int) -> bool:
        return RolModel.objects.filter(pk=id).exists()

    def _to_entity(self, model: RolModel) -> Rol:
        from datetime import datetime
        return Rol(
            id=model.pk,
            empresa_id=model.empresa_id,
            nombre=model.nombre,
            permisos=set(model.permisos),
            es_sistema=model.es_sistema,
            fecha_creacion=model.fecha_creacion,
        )