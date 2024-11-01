import os
from src.update_files.update_json import ROOT_PATH, UpdateJSON


def test_init_with_filepath():
    """Тест инициализации сейвера с пользовательским именем"""
    filename = "test.json"
    v_saver = UpdateJSON(filename)

    expected = os.path.join(ROOT_PATH, filename)
    result = v_saver.file_path

    assert result == expected


def test_add_and_get_vacancy(vacancies, capsys, vacancies_from_file):
    """Тест добавления вакансий в файл и их выгрузку"""
    v_saver = UpdateJSON()

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    message = capsys.readouterr()
    added_vacancy1 = message.out.strip().split("\n")[0]

    assert added_vacancy1 == "Вакансия 'Специалист по безопасности' добавлена в файл"

    expected = vacancies_from_file
    result = v_saver.get_vacancies(with_print=False)

    assert result == expected


def test_delete_vacancy(vacancies, capsys):
    """Тест удаления вакансий из файла"""
    v_saver = UpdateJSON()
    file_path = v_saver.file_path

    for vacancy in vacancies:
        v_saver.add_vacancy(vacancy)

    for vacancy in vacancies:
        v_saver.delete_vacancy(vacancy)

    message = capsys.readouterr()
    deleted_vacancy = message.out.strip().split("\n")[4]

    assert deleted_vacancy == f"Вакансия 'Специалист по безопасности' удалена из файла: {file_path}"

    result = v_saver.get_vacancies(with_print=False)

    assert result == []


def test_print_vacancies(vacancies_from_file, strings_for_print, capsys):
    """Тест вывода информации в консоль"""
    v_saver = UpdateJSON()
    v_saver.print_vacancies(vacancies_from_file)

    message = capsys.readouterr()
    printed_vacancies = message.out.strip().split("\n\n")

    for index in range(4):
        assert strings_for_print[index] in printed_vacancies[index]
