import re
from abc import ABC, abstractmethod
from typing import Any, Tuple, Union


class Validator(ABC):
    """Абстрактный класс для валидации данных вакансии"""

    @staticmethod
    @abstractmethod
    def validate(value: Any) -> Union[str, int, list, Tuple[int, int]]:
        """Абстрактный метод для валидации значения"""
        pass


class NameValidator(Validator):
    """Валидатор для названия вакансии"""

    @staticmethod
    def validate(value: str) -> str:
        """Проверяет, что название вакансии не пустое"""
        if not value:
            raise ValueError("Название вакансии не указано.")
        return value


class URLValidator(Validator):
    """Валидатор для URL вакансии"""

    @staticmethod
    def validate(value: str) -> str:
        """Проверяет, что URL вакансии не пустой и начинается с 'https://'"""
        if not value:
            raise ValueError("URL вакансии не указан.")
        if value.startswith("<") and value.endswith(">"):
            value = value[1:-1]
        if not value.startswith("https://"):
            raise ValueError("URL должен начинаться с 'https://'")
        return value


class RequirementsValidator(Validator):
    """Валидатор для требований к вакансии"""

    @staticmethod
    def validate(value: str) -> str:
        """Проверяет, что требования к вакансии указаны"""
        if not value:
            return "Требования не указаны."
        return value


class SalaryValidator(Validator):
    """Валидатор для зарплаты"""

    @staticmethod
    def validate(value: Union[str, int]) -> Union[Tuple[int, int], int]:
        """Проверяет корректность указания зарплаты"""
        if not value:
            return 0

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            pattern1 = r"(\d+)\D+"
            pattern2 = r"(\d+)\D+(\d+)"

            for pattern in (pattern2, pattern1):
                match = re.search(pattern, value.replace(" ", ""))

                if match:
                    if len(match.groups()) == 2:
                        return int(match.group(1)), int(match.group(2))
                    elif len(match.groups()) == 1:
                        return int(match.group(1))

        return 0


class AreaNameValidator(Validator):
    """Валидатор для названия города размещения вакансии"""

    @staticmethod
    def validate(value: str) -> str:
        """Проверяет, что название города размещения вакансии указано.
        Если информация не указана, используется 'Россия'"""
        if not value:
            return "Россия"
        return value


class SearchValidator(Validator):
    """Валидатор для названия города."""

    @staticmethod
    def validate(value: str) -> list:
        """Проверяет наличие названия города и возвращает название в виде списка"""
        parts_of_name = re.findall(r"\w+", value)

        if parts_of_name:
            return parts_of_name

        return []
