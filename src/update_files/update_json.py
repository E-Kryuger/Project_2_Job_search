import json
import os

from paths import ROOT_PATH, VACANCIES_JSON_PATH
from src.update_files.update_file import UpdateFile
from src.vacancy.vacancy import Vacancy


class UpdateJSON(UpdateFile):
    """Класс для работы с JSON-файлами"""

    def __init__(self, file_name=VACANCIES_JSON_PATH):
        """Конструктор"""
        if file_name != VACANCIES_JSON_PATH:
            if not file_name.endswith(".json"):
                file_name = file_name + ".json"
            file_name = os.path.join(
                ROOT_PATH,
                file_name,
            )

        self._file_path = file_name

    def add_vacancy(self, vacancy):
        """Добавляет вакансию в файл"""

        vacancy_json = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "city": vacancy.city,
            "requirements": vacancy.requirements,
        }

        vacancy_name = vacancy.name if len(vacancy.name) < 50 else vacancy.name[:50] + "..."
        vacancy_added = f"Вакансия '{vacancy_name}' добавлена в файл"

        if not os.path.exists(self._file_path):
            self._write_file([vacancy_json])
            print(vacancy_added)
            return

        vacancies_data = self._read_file()

        if vacancy.url in (vacancy_data["url"] for vacancy_data in vacancies_data):
            print(f"Вакансия '{vacancy_name}' уже существует в файле")
        else:
            vacancies_data.append(vacancy_json)
            self._write_file(vacancies_data)
            print(vacancy_added)

    def delete_vacancy(self, vacancy):
        """Метод для удаления вакансии из файла"""
        vacancy_name = vacancy.name if len(vacancy.name) < 50 else vacancy.name[:50] + "..."
        vacancies_data = self._read_file()

        for index, vacancy_data in enumerate(vacancies_data):
            if vacancy_data["url"] == vacancy.url:
                del vacancies_data[index]
                self._write_file(vacancies_data)
                print(f"Вакансия '{vacancy_name}' удалена из файла: {self._file_path}")
                return

        print(f"Вакансии '{vacancy_name}' нет в файле: {self._file_path}")

    def get_vacancies(self, with_print=True):
        """Метод для получения вакансий из файла"""
        vacancies = self._read_file()
        if vacancies:
            print(f"Количество вакансий в файле: {len(vacancies)}")
        else:
            print("В файле нет вакансий")

        if with_print and vacancies:
            self.print_vacancies(vacancies)

        return vacancies

    def _read_file(self):
        """Метод для чтения файлов"""
        try:
            with open(self._file_path, "r", encoding="utf-8") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def _write_file(self, vacancies_data):
        """Метод для записи информации о вакансии в файл"""
        with open(self._file_path, "w", encoding="utf-8") as file:
            json.dump(vacancies_data, file, ensure_ascii=False, indent=4)

    @staticmethod
    def print_vacancies(vacancies_data):
        """Метод для вывода информации о вакансии"""
        number_vacancy = 1
        for vacancy_data in vacancies_data:
            print(f"\nВакансия №{number_vacancy}\n---")
            print(f"Название вакансии: {vacancy_data['name']}")
            print(f"Ссылка на вакансию: {vacancy_data['url']}")
            print(f"Зарплата: {vacancy_data['salary']}")
            print(f"Размещение вакансии: {vacancy_data['city']}")
            print(f"Требования: {vacancy_data['requirements']}")
            print("==========")
            number_vacancy += 1

    @property
    def file_path(self):
        """Геттер для получения пути к файлу"""
        return self._file_path
