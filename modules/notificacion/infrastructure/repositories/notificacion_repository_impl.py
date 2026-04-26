from typing import Optional, List
from modules.notificacion.domain.entities.notificacion import Notificacion
from modules.notificacion.domain.repositories.notificacion_repository import NotificacionRepository
from modules.notificacion.infrastructure.models.notificacion_model import NotificacionModel


class DjangoNotificacionRepository(NotificacionRepository):
    def get_by_id(self, id: int) -> Optional[Notificacion]:
        try:
            return self._to_entity(NotificacionModel.objects.get(pk=id))
        except NotificacionModel.DoesNotExist:
            return None

    def get_by_usuario(
        self,
        usuario_id: int,
        solo_no_leidas: bool = False,
        page: int = 1,
        page_size: int = 20,
    ) -> List[Notificacion]:
        qs = NotificacionModel.objects.filter(usuario_id=usuario_id)
        if solo_no_leidas:
            qs = qs.filter(leida=False)
        offset = (page - 1) * page_size
        return [self._to_entity(m) for m in qs.order_by("-fecha_creacion")[offset: offset + page_size]]

    def save(self, notificacion: Notificacion) -> Notificacion:
        if notificacion.id:
            model = NotificacionModel.objects.get(pk=notificacion.id)
        else:
            model = NotificacionModel()

        model.empresa_id = notificacion.empresa_id
        model.usuario_id = notificacion.usuario_id
        model.titulo = notificacion.titulo
        model.mensaje = notificacion.mensaje
        model.canal = notificacion.canal
        model.leida = notificacion.leida
        model.enviada = notificacion.enviada
        model.fecha_envio = notificacion.fecha_envio
        model.fecha_lectura = notificacion.fecha_lectura
        model.save()

        notificacion.id = model.pk
        return notificacion

    def count_no_leidas(self, usuario_id: int) -> int:
        return NotificacionModel.objects.filter(usuario_id=usuario_id, leida=False).count()

    def _to_entity(self, model: NotificacionModel) -> Notificacion:
        return Notificacion(
            id=model.pk,
            empresa_id=model.empresa_id,
            usuario_id=model.usuario_id,
            titulo=model.titulo,
            mensaje=model.mensaje,
            canal=model.canal,
            leida=model.leida,
            enviada=model.enviada,
            fecha_envio=model.fecha_envio,
            fecha_lectura=model.fecha_lectura,
            fecha_creacion=model.fecha_creacion,
        )