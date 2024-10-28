from abc import ABC, abstractmethod


class GetVacanciesAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def _connect_to_api(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass
