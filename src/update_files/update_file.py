from abc import ABC, abstractmethod


class UpdateFile(ABC):
    """Абстрактный класс для работы с файлами"""

    @abstractmethod
    def add_vacancy(self):
        """Абстрактный метод добавления вакансии в файл"""
        pass

    @abstractmethod
    def delete_vacancy(self):
        """Абстрактный метод удаления вакансии из файла"""
        pass

    @abstractmethod
    def get_vacancies(self, with_print=True):
        """Абстрактный метод выгрузки вакансий из файла"""
        pass
