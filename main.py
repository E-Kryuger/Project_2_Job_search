from src.get_api.api_hh import HH
from src.utils.utils import create_list_of_vacancies, get_top_vacancies, initialization_menu, search_menu


def user_interaction():
    """Функция для взаимодействия с пользователем"""

    vacancies_saver = initialization_menu()
    vacancies_data = search_menu(hh_api=HH())
    if not vacancies_data:
        return
    vacancies_list = create_list_of_vacancies(vacancies_data)

    while True:
        choice = input(
            "==========\n\n"
            "Показать и сохранить:\n"
            "1 - Все найденные вакансии\n"
            "2 - Топ вакансий по размеру заработной платы\n"
            "Введите число: "
        ).strip()

        if choice == "1":
            break
        elif choice == "2":
            vacancies_list = get_top_vacancies(vacancies_list)
            break

    print("\n===== Сохранение вакансий =====")
    for vacancy in vacancies_list:
        vacancies_saver.add_vacancy(vacancy)
    print("==========")
    print("\n===== Вывод вакансий =====")
    vacancies_saver.get_vacancies()


if __name__ == "__main__":
    user_interaction()
