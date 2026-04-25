from typing import Optional, List
from datetime import datetime
from modules.auditoria.domain.entities.registro_auditoria import RegistroAuditoria
from modules.auditoria.domain.repositories.auditoria_repository import AuditoriaRepository
from modules.auditoria.infrastructure.models.auditoria_model import AuditoriaLogModel


class DjangoAuditoriaRepository(AuditoriaRepository):
    def get_by_id(self, id: int) -> Optional[RegistroAuditoria]:
        try:
            return self._to_entity(AuditoriaLogModel.objects.get(pk=id))
        except AuditoriaLogModel.DoesNotExist:
            return None

    def get_global(
        self,
        empresa_id: Optional[int] = None,
        usuario_id: Optional[int] = None,
        rol: Optional[str] = None,
        tipo_evento: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> List[RegistroAuditoria]:
        qs = AuditoriaLogModel.objects.all()
        if empresa_id is not None:
            qs = qs.filter(empresa_id=empresa_id)
        if usuario_id:
            qs = qs.filter(usuario_id=usuario_id)
        if rol:
            qs = qs.filter(rol_usuario=rol)
        if tipo_evento:
            qs = qs.filter(tipo_evento=tipo_evento)
        if fecha_desde:
            qs = qs.filter(timestamp__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(timestamp__lte=fecha_hasta)
        offset = (page - 1) * page_size
        return [self._to_entity(m) for m in qs[offset: offset + page_size]]

    def get_by_empresa(
        self,
        empresa_id: int,
        usuario_id: Optional[int] = None,
        tipo_evento: Optional[str] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> List[RegistroAuditoria]:
        return self.get_global(
            empresa_id=empresa_id,
            usuario_id=usuario_id,
            tipo_evento=tipo_evento,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            page=page,
            page_size=page_size,
        )

    def save(self, registro: RegistroAuditoria) -> RegistroAuditoria:
        model = AuditoriaLogModel(
            empresa_id=registro.empresa_id,
            usuario_id=registro.usuario_id,
            rol_usuario=registro.rol_usuario,
            tipo_evento=registro.tipo_evento,
            descripcion=registro.descripcion,
            ip_address=registro.ip_address,
            detalles=registro.detalles,
        )
        model.save()
        return self._to_entity(model)

    def count_global(
        self,
        empresa_id: Optional[int] = None,
        fecha_desde: Optional[datetime] = None,
        fecha_hasta: Optional[datetime] = None,
    ) -> int:
        qs = AuditoriaLogModel.objects.all()
        if empresa_id is not None:
            qs = qs.filter(empresa_id=empresa_id)
        if fecha_desde:
            qs = qs.filter(timestamp__gte=fecha_desde)
        if fecha_hasta:
            qs = qs.filter(timestamp__lte=fecha_hasta)
        return qs.count()

    def eliminar_anteriores_a(self, fecha_limite: datetime) -> int:
        count, _ = AuditoriaLogModel.objects.filter(timestamp__lt=fecha_limite).delete()
        return count

    def _to_entity(self, model: AuditoriaLogModel) -> RegistroAuditoria:
        return RegistroAuditoria(
            id=model.pk,
            empresa_id=model.empresa_id,
            usuario_id=model.usuario_id,
            rol_usuario=model.rol_usuario,
            tipo_evento=model.tipo_evento,
            descripcion=model.descripcion,
            ip_address=model.ip_address,
            detalles=model.detalles,
            timestamp=model.timestamp,
        )