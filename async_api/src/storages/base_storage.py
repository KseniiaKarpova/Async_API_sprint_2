from abc import abstractmethod, ABC
from uuid import UUID


class BaseStorage(ABC):
    @abstractmethod
    async def get_data_list(self, page_number: int, page_size: int):
        pass

    @abstractmethod
    async def get_data_by_id(self, id: UUID):
        pass
