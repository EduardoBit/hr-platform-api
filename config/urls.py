from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('modules.usuario.interfaces.urls')),
    path('api/empresas/', include('modules.empresa.interfaces.urls')),
    path('api/empleados/', include('modules.empleado.interfaces.urls')),
    path('api/asistencia/', include('modules.asistencia.interfaces.urls')),
    path('api/solicitudes/', include('modules.solicitud.interfaces.urls')),
    path('api/auditoria/', include('modules.auditoria.interfaces.urls')),
    path('api/notificaciones/', include('modules.notificacion.interfaces.urls')),
    path('api/suscripciones/', include('modules.suscripcion.interfaces.urls')),
]
