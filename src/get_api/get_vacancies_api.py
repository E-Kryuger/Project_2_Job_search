from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import requests


class GetVacanciesAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_to_api(self) -> Optional[requests.Response]:
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, city_name: str) -> List[Dict]:
        pass
