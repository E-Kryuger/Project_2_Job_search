from src.utils.validator import AreaNameValidator, NameValidator, RequirementsValidator, SalaryValidator, URLValidator


class Vacancy:
    """Класс для представления информации о вакансии"""

    __slots__ = ("_name", "_url", "_salary", "_city", "_requirements")

    def __init__(self, name="", url="", salary=0, city="", requirements=""):
        """Конструктор для инициализации объекта вакансии с валидацией данных"""
        try:
            self._name = NameValidator.validate(name)
            self._url = URLValidator.validate(url)
        except ValueError as e:
            print(f"Ошибка при инициализации объекта: {e}")
            self._name = ""
            self._url = ""
            self._salary = 0
            self._city = ""
            self._requirements = ""
        else:
            self._requirements = RequirementsValidator.validate(requirements)
            self._salary = SalaryValidator.validate(salary)
            self._city = AreaNameValidator.validate(city)

    def _avg_salary(self):
        """Метод, использующийся при сравнении зарплат.
        Делает расчет средней зарплаты, если указаны диапазоны"""
        if isinstance(self._salary, tuple):
            return round(sum(self._salary) / 2, 2)
        return self._salary

    @staticmethod
    def _validate_other(other):
        """Метод для проверки является ли другой объект экземпляром класса Vacancy"""
        if not isinstance(other, Vacancy):
            raise TypeError("Сравнение возможно только между объектами Vacancy.")
        return True

    def __lt__(self, other):
        """Дандер для сравнения вакансий по зарплате"""
        self._validate_other(other)
        return self._avg_salary() < other._avg_salary()

    def __str__(self):
        """Дандер для строкового представления вакансии"""
        return (
            f"Название вакансии: {self._name}\n"
            f"Ссылка на вакансию: {self._url}\n"
            f"Зарплата: {self.salary}\n"
            f"Локация размещения вакансии: {self.city}\n"
            f"Требования: {self._requirements}"
        )

    # Геттеры и сеттеры
    @property
    def name(self):
        """Геттер для получения названия вакансии"""
        return self._name

    @name.setter
    def name(self, value):
        """Сеттер названия вакансии с валидацией"""
        self._name = NameValidator.validate(value)

    @property
    def url(self):
        """Геттер для получения URL вакансии"""
        return self._url

    @url.setter
    def url(self, value):
        """Сеттер URL вакансии с валидацией"""
        self._url = URLValidator.validate(value)

    @property
    def salary(self):
        """Геттер для получения зарплаты в виде строки"""
        salary = self._salary
        if isinstance(salary, int):
            return f"{salary} руб."
        return f"{salary[0]}-{salary[1]} руб."

    @salary.setter
    def salary(self, value):
        """Сеттер зарплаты с валидацией"""
        self._salary = SalaryValidator.validate(value)

    @property
    def city(self):
        """Геттер для получения названия города размещения вакансии"""
        return self._city

    @city.setter
    def city(self, value):
        """Сеттер названия города"""
        self._city = AreaNameValidator.validate(value)

    @property
    def requirements(self):
        """Геттер для получения требований вакансии"""
        return self._requirements

    @requirements.setter
    def requirements(self, value):
        """Сеттер требований вакансии с валидацией"""
        self._requirements = RequirementsValidator.validate(value)