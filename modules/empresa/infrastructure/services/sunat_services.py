import requests
from django.conf import settings
from shared.domain.exceptions import ExternalServiceException
from shared.domain.value_objects import Ruc
from modules.empresa.domain.exceptions import RucInvalidoException


class SunatService:
    def __init__(self):
        self._api_url = settings.SUNAT_API_URL
        self._token = settings.SUNAT_API_TOKEN
        self._timeout = 10

    def consultar_ruc(self, ruc: str) -> dict:
        Ruc(ruc)
        try:
            response = requests.get(
                f"{self._api_url}/{ruc}",
                headers={"Authorization": f"Bearer {self._token}"},
                timeout=self._timeout,
            )
        except requests.exceptions.Timeout:
            raise ExternalServiceException("SUNAT", "tiempo de espera agotado.")
        except requests.exceptions.ConnectionError:
            raise ExternalServiceException("SUNAT", "no se pudo establecer conexión.")

        if response.status_code == 404:
            raise RucInvalidoException(ruc)

        if not response.ok:
            raise ExternalServiceException("SUNAT", f"código de respuesta {response.status_code}.")

        data = response.json()

        if data.get("estadoContribuyente") != "ACTIVO":
            raise RucInvalidoException(ruc)

        return {
            "ruc": ruc,
            "razon_social": data.get("razonSocial", ""),
            "nombre_comercial": data.get("nombreComercial") or data.get("razonSocial", ""),
            "direccion": data.get("domicilioFiscal", ""),
            "estado": data.get("estadoContribuyente", ""),
        }