from src.utils.validator import SalaryValidator
from src.vacancy.vacancy import Vacancy
from src.update_files.update_json import UpdateJSON
from src.get_api.api_hh import HH


def avg_salary(salary_str):
    """Функция для получения среднего значения из строки"""
    salary = SalaryValidator.validate(salary_str)
    if isinstance(salary, tuple):
        salary_avg = sum(salary) / 2
        return round(salary_avg, 2)
    return salary


def get_avg_salary(vacancy):
    """Функция для получения зарплаты из объекта вакансии в виде числа"""
    return avg_salary(vacancy.salary)


def sort_by_salary(vacancies_list, descending=True):
    """Функция для сортировки списка вакансий"""
    return sorted(vacancies_list, key=get_avg_salary, reverse=descending)


def get_top_vacancies(vacancies):
    """Функция, выводящая топ N вакансий"""
    sorted_vacancies = sort_by_salary(vacancies)
    quantity = len(sorted_vacancies)
    while True:
        top_n_str = input("Введите число: Какое количество вакансий интересует? Вывести Топ-").strip()
        if top_n_str.isdigit():
            top_n = int(top_n_str)
            if top_n > quantity:
                print(f"Нет возможности получения 'Топ-{top_n}'")
                print(f"Всего найдено вакансий: {quantity}")
                continue
            break

    return sorted_vacancies[:top_n]


def get_salary(salary_dict):
    """Функция для подготовки информации о зарплате к инициализации объекта Vacancy"""
    if salary_dict:
        from_ = salary_dict["from"]
        to_ = salary_dict["to"]

        if isinstance(from_, int) and isinstance(to_, int):
            return f"{from_}-{to_} руб."
        elif isinstance(from_, int):
            return f"{from_} руб."
        elif isinstance(to_, int):
            return f"{to_} руб."

    return "0 руб."


def create_list_of_vacancies(data_from_api):
    """Функция для создания списка объектов вакансий из данных, полученных от API"""
    vacancies_list = []

    for vacancy_data in data_from_api:
        name = vacancy_data["name"]
        url = vacancy_data["alternate_url"]
        salary = get_salary(vacancy_data["salary"])
        city = vacancy_data.get("area", {}).get("name")
        requirements = vacancy_data["snippet"]["requirement"]

        vacancies_list.append(Vacancy(name, url, salary, city, requirements))

    return vacancies_list


def initialization_menu():
    """Функция для выбора имений файла, в который будут сохраняться вакансии"""
    while True:
        choice = input("===== Настройка поиска =====\n"
                       "Хотите использовать системное имя файла для хранения вакансий?\n"
                       "1 - Да\n"
                       "2 - Нет\n"
                       "Введите число: ")

        if choice == "1":
            print("\nИспользуется стандартное имя файла: vacancies.json")
            return UpdateJSON()
        elif choice == "2":
            filename = input("Введите имя файла: ").strip()
            if not filename.endswith(".json"):
                filename += ".json"
            print(f"\nИспользуется имя файла: {filename}")
            return UpdateJSON(filename)


def search_menu(hh_api):
    """Функция для выбора города поиска вакансий"""
    while True:
        choice = input("\nХотите искать вакансии по всей России?\n "
                       "1 - Да\n "
                       "2 - Нет, хочу указать город для поиска\n "
                       "Введите число: ")

        if choice == "1":
            result = search_vacancies(hh_api, search_in_city=False)
            return result
        elif choice == "2":
            result = search_vacancies(hh_api, search_in_city=True)
            return result


def search_vacancies(hh_api, search_in_city):
    """Вспомогательная функция для поиска вакансий"""
    if search_in_city:
        city_name = input("\nНазвание города: ").strip()
    query = input("\nКлючевое слово для поиска: ")

    print("==========\n\n"
          "Подождите, ваш запрос обрабатывается...")

    if search_in_city:
        vacancies = hh_api.get_vacancies(query, city_name)
    else:
        vacancies = hh_api.get_vacancies(query)

    print("\nРезультат поиска:"
          "")
    if vacancies:
        quantity = len(vacancies)
        print(f"Количество вакансий найденных по запросу '{query}': {quantity}")
        return vacancies
    else:
        print(f"По запросу '{query}' ничего не найдено")
        return []

