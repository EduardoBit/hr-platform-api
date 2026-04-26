from abc import ABC, abstractmethod
from typing import Optional, List
from modules.empresa.domain.entities.sede import Sede


class SedeRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Sede]:
        raise NotImplementedError

    @abstractmethod
    def get_by_empresa(self, empresa_id: int) -> List[Sede]:
        raise NotImplementedError

    @abstractmethod
    def save(self, sede: Sede) -> Sede:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists(self, id: int) -> bool:
        raise NotImplementedError