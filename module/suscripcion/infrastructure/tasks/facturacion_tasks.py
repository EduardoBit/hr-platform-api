from celery import shared_task
from shared.constants import TRIAL_ALERT_DAYS_BEFORE


@shared_task(name="suscripcion.verificar_trials_por_vencer")
def verificar_trials_por_vencer():
    from modules.suscripcion.infrastructure.repositories.suscripcion_repository_impl import DjangoSuscripcionRepository
    from modules.empresa.infrastructure.repositories.empresa_repository_impl import DjangoEmpresaRepository
    from modules.notificacion.infrastructure.services.email_service import EmailService

    suscripcion_repo = DjangoSuscripcionRepository()
    empresa_repo = DjangoEmpresaRepository()
    email_service = EmailService()

    suscripciones = suscripcion_repo.get_trials_por_vencer(TRIAL_ALERT_DAYS_BEFORE)

    for suscripcion in suscripciones:
        empresa = empresa_repo.get_by_id(suscripcion.empresa_id)
        if not empresa:
            continue
        from datetime import datetime
        dias_restantes = max(0, (suscripcion.fecha_fin_trial - datetime.now()).days)
        email_service.enviar(
            destinatario=str(empresa.correo),
            asunto="Tu periodo de prueba está por vencer — SisRRHH",
            cuerpo=(
                f"Estimado cliente de {empresa.razon_social},\n\n"
                f"Tu periodo de prueba vence en {dias_restantes} día(s).\n"
                f"Activa tu suscripción para continuar usando SisRRHH sin interrupciones.\n\n"
                f"Equipo SisRRHH"
            ),
        )


@shared_task(name="suscripcion.suspender_por_pago_vencido")
def suspender_por_pago_vencido():
    from modules.suscripcion.infrastructure.repositories.suscripcion_repository_impl import DjangoSuscripcionRepository
    from modules.empresa.infrastructure.repositories.empresa_repository_impl import DjangoEmpresaRepository
    from modules.notificacion.infrastructure.services.email_service import EmailService
    from modules.suscripcion.application.use_cases.suspender_por_pago import SuspenderPorPagoUseCase

    class _NotifAdapter:
        def __init__(self, email_svc):
            self._email = email_svc

        def notificar_suspension_por_pago(self, correo, empresa_nombre):
            self._email.notificar_suspension_por_pago(correo, empresa_nombre)

    use_case = SuspenderPorPagoUseCase(
        suscripcion_repository=DjangoSuscripcionRepository(),
        empresa_repository=DjangoEmpresaRepository(),
        notificacion_use_case=_NotifAdapter(EmailService()),
    )
    use_case.execute()


@shared_task(name="suscripcion.activar_suscripciones_trial_vencidas")
def activar_suscripciones_trial_vencidas():
    from datetime import datetime
    from modules.suscripcion.infrastructure.repositories.suscripcion_repository_impl import DjangoSuscripcionRepository
    from shared.constants import EstadosSuscripcion

    repo = DjangoSuscripcionRepository()
    from modules.suscripcion.infrastructure.models.suscripcion_model import SuscripcionModel

    vencidas = SuscripcionModel.objects.filter(
        estado=EstadosSuscripcion.TRIAL,
        fecha_fin_trial__lt=datetime.now(),
    )
    for model in vencidas:
        suscripcion = repo._to_entity(model)
        suscripcion.vencer()
        repo.save(suscripcion)