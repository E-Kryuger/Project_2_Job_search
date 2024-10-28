import re

import requests

from src.get_api.get_vacancies_api import GetVacanciesAPI
from src.utils.validator import SearchValidator


# Константы
API_URL = "https://api.hh.ru/vacancies"
HEADERS = {"User-Agent": "HH-User-Agent"}
DEFAULT_AREA_ID = 113  # По умолчанию — Россия
DEFAULT_AREA_URL = "https://api.hh.ru/areas/113"


class HH(GetVacanciesAPI):
    """Класс для работы с API HH.ru"""

    def __init__(self):
        """Конструктор для инициализации объекта, работающего с API"""
        self.__url = API_URL
        self.__headers = HEADERS
        self.__params = {
            "text": "",
            "area": DEFAULT_AREA_ID,
            "page": 0,
            "per_page": 100,
            "only_with_salary": "true",
        }
        self.__vacancies = []

    def _connect_to_api(self):
        """Подключение к API и проверка успешности подключения"""
        try:
            response = requests.get(url=self.__url, headers=self.__headers)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Ошибка при подключении к API: {e}")
            return None
        else:
            return response

    def get_vacancies(self, keyword, city_name="", with_salary=True):
        """Получение вакансий по ключевому слову и городу(опционально)"""
        if not self._connect_to_api():
            return []  # Возврат пустого списка в случае ошибки подключения

        self.__params["text"] = keyword
        self.__params["area"] = self._get_area_id(city_name) if city_name else DEFAULT_AREA_ID
        self.__params["only_with_salary"] = "false" if not with_salary else "true"
        self.__params["page"] = 0

        # Запуск цикла для перебора страниц
        while self.__params["page"] is not None and self.__params["page"] != 20:
            try:
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                response.raise_for_status()
                part_of_vacancies = response.json().get("items", [])
            except requests.RequestException as e:
                print(f"Ошибка при запросе вакансий: {e}")
                break
            else:
                if not part_of_vacancies:
                    break
                self.__vacancies.extend(part_of_vacancies)
                self.__params["page"] = int(self.__params["page"]) + 1

        return self.__vacancies

    @staticmethod
    def _get_area_id(city_name: str) -> int:
        """Получение ID города"""
        # Валидация города перед поиском ID
        name = SearchValidator.validate(city_name)
        not_found = f"Не удалось найти город '{city_name}'. Поиск вакансий будет осуществлен по всей России."
        if not name:
            print(not_found)
            return DEFAULT_AREA_ID

        pattern = r"\b(?:" + "|".join(re.escape(n) for n in name) + r")\b"
        regex = re.compile(pattern, re.IGNORECASE)  # Объект шаблона для поиска

        try:
            response = requests.get(DEFAULT_AREA_URL)
            response.raise_for_status()
            regions = response.json().get("areas", [])
        except requests.RequestException as e:
            print(f"Ошибка при запросе областей: {e}")
        else:
            for region in regions:
                region_name = set(regex.findall(region["name"]))
                # Проверка полного совпадения словесных частей названия города
                if all(n.lower() in (rn.lower() for rn in region_name) for n in name):
                    return int(region["id"])

                for city_ in region["areas"]:
                    city_full_name = set(regex.findall(city_["name"]))
                    # Проверка полного совпадения словесных частей названия города
                    if all(n.lower() in (cfn.lower() for cfn in city_full_name) for n in name):
                        return int(city_["id"])

        print(not_found)
        return DEFAULT_AREA_ID
