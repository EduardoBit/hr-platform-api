from celery import shared_task


@shared_task(name="solicitud.notificar_solicitudes_pendientes")
def notificar_solicitudes_pendientes():
    from modules.solicitud.infrastructure.models.solicitud_model import SolicitudModel
    from modules.empresa.infrastructure.repositories.empresa_repository_impl import DjangoEmpresaRepository
    from modules.empleado.infrastructure.repositories.empleado_repository_impl import DjangoEmpleadoRepository
    from modules.notificacion.infrastructure.services.email_service import EmailService
    from shared.constants import EstadosSolicitud
    from datetime import datetime, timedelta

    empresa_repo = DjangoEmpresaRepository()
    empleado_repo = DjangoEmpleadoRepository()
    email_service = EmailService()

    hace_24h = datetime.now() - timedelta(hours=24)
    pendientes = SolicitudModel.objects.filter(
        estado=EstadosSolicitud.PENDIENTE,
        fecha_creacion__lte=hace_24h,
    ).select_related("tipo_permiso")

    for solicitud_model in pendientes:
        empleado = empleado_repo.get_by_id(solicitud_model.empleado_id)
        if not empleado:
            continue
        empresa = empresa_repo.get_by_id(solicitud_model.empresa_id)
        if not empresa:
            continue
        email_service.enviar(
            destinatario=str(empresa.correo),
            asunto=f"Solicitud pendiente de revisión — {solicitud_model.tipo_permiso_nombre}",
            cuerpo=(
                f"Existe una solicitud de {solicitud_model.tipo_permiso_nombre} "
                f"del empleado {empleado.nombre_completo()} pendiente de revisión por más de 24 horas.\n"
                f"Período: {solicitud_model.fecha_inicio} al {solicitud_model.fecha_fin}.\n\n"
                f"Ingrese a la plataforma para evaluarla.\n\nEquipo NexusRH"
            ),
        )


@shared_task(name="solicitud.limpiar_solicitudes_canceladas")
def limpiar_solicitudes_canceladas():
    from modules.solicitud.infrastructure.models.solicitud_model import SolicitudModel
    from shared.constants import EstadosSolicitud
    from datetime import datetime, timedelta

    hace_90_dias = datetime.now() - timedelta(days=90)
    SolicitudModel.objects.filter(
        estado__in=[EstadosSolicitud.CANCELADA, EstadosSolicitud.RECHAZADA],
        fecha_actualizacion__lt=hace_90_dias,
    ).delete()