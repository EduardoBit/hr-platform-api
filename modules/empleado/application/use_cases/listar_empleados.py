from typing import List, Any
from shared.application.base_use_case import BaseUseCase
from modules.empleado.domain.repositories.empleado_repository import EmpleadoRepository
from modules.empleado.application.dtos.empleado_dto import ListarEmpleadosInputDTO, EmpleadoOutputDTO

class ListarEmpleadosUseCase(BaseUseCase[ListarEmpleadosInputDTO, List[EmpleadoOutputDTO]]):
    def __init__(self, empleado_repository: EmpleadoRepository, sede_repository: Any = None):
        self._empleado_repository = empleado_repository
        self._sede_repository = sede_repository

    def execute(self, input_dto: ListarEmpleadosInputDTO) -> List[EmpleadoOutputDTO]:
        empleados = self._empleado_repository.get_by_empresa(
            empresa_id=input_dto.empresa_id,
            estado=input_dto.estado,
            area=input_dto.area,
            sede_id=input_dto.sede_id,
            search=input_dto.search,
            page=input_dto.page,
            page_size=input_dto.page_size,
        )

        lista_empleados = []
        if isinstance(empleados, dict) and "results" in empleados:
            lista_empleados = empleados["results"]
        elif hasattr(empleados, 'results'):
            lista_empleados = empleados.results
        else:
            lista_empleados = empleados

        sedes_cache = {}
        resultados = []

        for e in lista_empleados:
            sede_nombre = None
            if self._sede_repository and e.sede_id:
                if e.sede_id not in sedes_cache:
                    try:
                        # 1. Imprimimos en la consola del backend para ver la verdad
                        print(f"\n[DEBUG] --- BUSCANDO SEDE ID: {e.sede_id} ---")
                        sede = self._sede_repository.get_by_id(e.sede_id)
                        print(f"[DEBUG] Resultado de la base de datos: {sede}")
                        
                        if sede:
                            # 2. Blindamos la extracción del nombre (sea diccionario u objeto, nombre o name)
                            if isinstance(sede, dict):
                                nombre = sede.get('nombre', sede.get('name', f"Sede ID {e.sede_id}"))
                            else:
                                nombre = getattr(sede, 'nombre', getattr(sede, 'name', f"Sede ID {e.sede_id}"))
                            
                            sedes_cache[e.sede_id] = str(nombre)
                        else:
                            sedes_cache[e.sede_id] = "No encontrada en BD"
                            
                    except Exception as err:
                        print(f"[DEBUG] Error al buscar la sede: {err}")
                        # Si get_by_id falla, evitamos que la API colapse
                        sedes_cache[e.sede_id] = "Error de repositorio"
                        
                sede_nombre = sedes_cache.get(e.sede_id)

            resultados.append(
                EmpleadoOutputDTO(
                    id=e.id,
                    empresa_id=e.empresa_id,
                    codigo_unico=str(e.codigo_unico),
                    nombres=e.nombres,
                    apellidos=e.apellidos,
                    tipo_documento=e.documento.tipo,
                    numero_documento=e.documento.value,
                    correo=str(e.correo),
                    cargo=e.cargo,
                    area=e.area,
                    sede_id=e.sede_id,
                    sede_nombre=sede_nombre,
                    estado=e.estado,
                    fecha_ingreso=e.fecha_ingreso,
                    fecha_creacion=e.fecha_creacion,
                )
            )

        return resultados