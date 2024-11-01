import pytest


def test_vacancy_init_with_all_arguments(vacancies):
    """Тест инициализации объекта со всеми атрибутами"""
    vacancy1 = vacancies[0]
    vacancy2 = vacancies[1]

    assert vacancy1.name == "Специалист по безопасности"
    assert vacancy1.url == "https://hh.ru/vacancy/108170610"
    assert vacancy1.salary == "2000000-2000000 руб."
    assert vacancy1.city == "Самара"
    assert vacancy1.requirements == "Умение работать на результат."

    assert vacancy2.name == "Директор управляющей компании"
    assert vacancy2.url == "https://hh.ru/vacancy/106661525"
    assert vacancy2.salary == "1950000 руб."
    assert vacancy2.city == "Москва"
    assert vacancy2.requirements == "Образование высшее (желательно управление предприятием)"


def test_vacancy_init_without_requirements(vacancies):
    """Тест инициализации объекта без вода данных для атрибута requirements"""
    vacancy = vacancies[2]

    assert vacancy.name == "Помощник чародея"
    assert vacancy.url == "https://hh.ru/vacancy/101935376"
    assert vacancy.salary == "1555000 руб."
    assert vacancy.city == "Красная Поляна"
    assert vacancy.requirements == "Требования не указаны."


def test_vacancy_init_without_salary(vacancies):
    """Тест инициализации объекта без вода данных для атрибута salary"""
    vacancy = vacancies[3]

    assert vacancy.name == "Помощник (Помощница) по бизнесу, по дому, в поездках"
    assert vacancy.url == "https://hh.ru/vacancy/109096851"
    assert vacancy.salary == "0 руб."
    assert vacancy.city == "Уфа"
    assert vacancy.requirements == "Проектное позитивное мышление аналитический склад ума"


def test_vacancy_str(vacancies):
    """Тест строкового представления объекта"""
    vacancy = vacancies[0]
    print(str(vacancy))
    assert str(vacancy) == (
        "Название вакансии: Специалист по безопасности\n"
        "Ссылка на вакансию: https://hh.ru/vacancy/108170610\n"
        "Зарплата: 2000000-2000000 руб.\n"
        "Локация размещения вакансии: Самара\n"
        "Требования: Умение работать на результат."
    )


def test_vacancy_lt(vacancies):
    """Тест сравнения объектов по зарплате"""
    v1, v2 = vacancies[:2]

    assert v2 < v1  # True
    assert not v1 < v2  # False

    assert not v2 > v1  # False
    assert v1 > v2  # True


def test_vacancy_lt_error(vacancies):
    """Тест сравнение вакансии с объектом, который не является экземпляром класса Vacancy"""
    vacancy = vacancies[0]

    with pytest.raises(TypeError) as exc_info:
        vacancy < 100_000

    assert str(exc_info.value) == "Сравнение возможно только между объектами Vacancy."
