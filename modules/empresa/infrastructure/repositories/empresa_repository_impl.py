from typing import Optional, List
from datetime import datetime
from shared.domain.value_objects import Email, Ruc
from modules.empresa.domain.entities.empresa import Empresa
from modules.empresa.domain.repositories.empresa_repository import EmpresaRepository
from modules.empresa.infrastructure.models.empresa_model import EmpresaModel


class DjangoEmpresaRepository(EmpresaRepository):
    def get_by_id(self, id: int) -> Optional[Empresa]:
        try:
            return self._to_entity(EmpresaModel.objects.get(pk=id))
        except EmpresaModel.DoesNotExist:
            return None

    def get_by_ruc(self, ruc: str) -> Optional[Empresa]:
        try:
            return self._to_entity(EmpresaModel.objects.get(ruc=ruc))
        except EmpresaModel.DoesNotExist:
            return None

    def get_all(self, estado: Optional[str] = None, page: int = 1, page_size: int = 20) -> List[Empresa]:
        qs = EmpresaModel.objects.all()
        if estado:
            qs = qs.filter(estado=estado)
        offset = (page - 1) * page_size
        return [self._to_entity(m) for m in qs[offset: offset + page_size]]

    def save(self, empresa: Empresa) -> Empresa:
        if empresa.id:
            model = EmpresaModel.objects.get(pk=empresa.id)
        else:
            model = EmpresaModel()

        model.ruc = str(empresa.ruc)
        model.razon_social = empresa.razon_social
        model.nombre_comercial = empresa.nombre_comercial
        model.correo = str(empresa.correo)
        model.telefono = empresa.telefono
        model.direccion = empresa.direccion
        model.logo_url = empresa.logo_url
        model.estado = empresa.estado
        model.fecha_actualizacion = empresa.fecha_actualizacion
        model.save()

        empresa.id = model.pk
        return empresa

    def exists_by_ruc(self, ruc: str) -> bool:
        return EmpresaModel.objects.filter(ruc=ruc).exists()

    def count_all(self, estado: Optional[str] = None) -> int:
        qs = EmpresaModel.objects.all()
        if estado:
            qs = qs.filter(estado=estado)
        return qs.count()

    def _to_entity(self, model: EmpresaModel) -> Empresa:
        return Empresa(
            id=model.pk,
            ruc=Ruc(model.ruc),
            razon_social=model.razon_social,
            nombre_comercial=model.nombre_comercial,
            correo=Email(model.correo),
            telefono=model.telefono,
            direccion=model.direccion,
            logo_url=model.logo_url,
            estado=model.estado,
            fecha_registro=model.fecha_registro,
            fecha_actualizacion=model.fecha_actualizacion,
        )