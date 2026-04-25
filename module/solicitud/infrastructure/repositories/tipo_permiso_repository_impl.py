from typing import Optional, List
from modules.solicitud.domain.entities.tipo_permiso import TipoPermiso
from modules.solicitud.domain.repositories.tipo_permiso_repository import TipoPermisoRepository
from modules.solicitud.infrastructure.models.tipo_permiso_model import TipoPermisoModel


class DjangoTipoPermisoRepository(TipoPermisoRepository):
    def get_by_id(self, id: int) -> Optional[TipoPermiso]:
        try:
            return self._to_entity(TipoPermisoModel.objects.get(pk=id))
        except TipoPermisoModel.DoesNotExist:
            return None

    def get_by_empresa(self, empresa_id: int, solo_activos: bool = True) -> List[TipoPermiso]:
        qs = TipoPermisoModel.objects.filter(empresa_id=empresa_id)
        if solo_activos:
            qs = qs.filter(es_activo=True)
        return [self._to_entity(m) for m in qs]

    def save(self, tipo_permiso: TipoPermiso) -> TipoPermiso:
        if tipo_permiso.id:
            model = TipoPermisoModel.objects.get(pk=tipo_permiso.id)
        else:
            model = TipoPermisoModel()

        model.empresa_id = tipo_permiso.empresa_id
        model.nombre = tipo_permiso.nombre
        model.descripcion = tipo_permiso.descripcion
        model.requiere_adjunto = tipo_permiso.requiere_adjunto
        model.es_activo = tipo_permiso.es_activo
        model.fecha_actualizacion = tipo_permiso.fecha_actualizacion
        model.save()

        tipo_permiso.id = model.pk
        return tipo_permiso

    def exists(self, id: int) -> bool:
        return TipoPermisoModel.objects.filter(pk=id).exists()

    def _to_entity(self, model: TipoPermisoModel) -> TipoPermiso:
        return TipoPermiso(
            id=model.pk,
            empresa_id=model.empresa_id,
            nombre=model.nombre,
            descripcion=model.descripcion,
            requiere_adjunto=model.requiere_adjunto,
            es_activo=model.es_activo,
            fecha_creacion=model.fecha_creacion,
            fecha_actualizacion=model.fecha_actualizacion,
        )