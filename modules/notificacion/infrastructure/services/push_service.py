class PushService:
    def enviar_websocket(self, usuario_id: int, titulo: str, mensaje: str, datos: dict = None) -> None:
        try:
            from channels.layers import get_channel_layer
            from asgiref.sync import async_to_sync
            channel_layer = get_channel_layer()
            if channel_layer is None:
                return
            async_to_sync(channel_layer.group_send)(
                f"user_{usuario_id}",
                {
                    "type": "notificacion.push",
                    "titulo": titulo,
                    "mensaje": mensaje,
                    "datos": datos or {},
                },
            )
        except Exception:
            pass
