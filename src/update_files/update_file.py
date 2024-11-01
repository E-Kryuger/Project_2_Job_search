from abc import ABC, abstractmethod
from typing import Dict

from src.vacancy.vacancy import Vacancy


class UpdateFile(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Абстрактный метод добавления вакансии в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Абстрактный метод удаления вакансии из файла"""
        pass

    @abstractmethod
    def get_vacancies(self, with_print: bool = True) -> Dict:
        """Абстрактный метод выгрузки вакансий из файла"""
        pass
