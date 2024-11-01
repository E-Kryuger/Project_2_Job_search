from unittest.mock import patch

from src.utils.utils import get_top_vacancies, create_list_of_vacancies, get_salary


@patch("builtins.input", side_effect=["2"])
def test_get_top_vacancies(mock_input, vacancies):
    """Тест функции, выводящей топ-N вакансий"""
    result = [vacancy.name for vacancy in get_top_vacancies(vacancies)]
    expected = ["Специалист по безопасности", "Директор управляющей компании"]

    assert result == expected
    mock_input.assert_called_once_with("Введите число: Какое количество вакансий интересует? Вывести Топ-")


def test_get_salary(json_data_items, vacancies_from_file):
    """Тест функции, подготавливающей информацию о зарплате к инициализации объекта Vacancy"""
    for index in range(4):
        salary_from_json = json_data_items[index]["salary"]
        expected_salary = vacancies_from_file[index]["salary"]

        assert get_salary(salary_from_json) == expected_salary


def test_create_list_of_vacancies(json_data_items, vacancies):
    """Тест утилиты, отвечающей за создание списка объектов вакансий из данных, полученных от API"""
    vacancies_list = create_list_of_vacancies(json_data_items)

    for index in range(4):
        created_vacancy = vacancies_list[index]
        expected_vacancy = vacancies[index]

        assert created_vacancy.name == expected_vacancy.name
        assert created_vacancy.url == expected_vacancy.url
        assert created_vacancy.salary == expected_vacancy.salary
        assert created_vacancy.city == expected_vacancy.city
        assert created_vacancy.requirements == expected_vacancy.requirements
