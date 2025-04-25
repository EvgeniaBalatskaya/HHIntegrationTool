from dataclasses import dataclass
from typing import Optional


@dataclass
class Vacancy:
    """Класс для представления вакансии с методами сравнения"""

    title: str
    url: str
    salary_from: Optional[int]
    salary_to: Optional[int]
    description: str
    requirements: str

    def __post_init__(self):
        """Валидация данных после инициализации"""
        self.__validate_salary()

    def __validate_salary(self):
        """Приватный метод валидации зарплаты"""
        if self.salary_from is None:
            self.salary_from = 0
        if self.salary_to is None:
            self.salary_to = 0

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий по минимальной зарплате"""
        return self.salary_from < other.salary_from

    def __gt__(self, other: "Vacancy") -> bool:
        """Сравнение вакансий по минимальной зарплате"""
        return self.salary_from > other.salary_from

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        """
        Преобразование списка словарей в список объектов Vacancy

        :param data: Список вакансий в формате JSON
        :return: Список объектов Vacancy
        """
        vacancies = []
        for item in data:
            salary = item.get("salary", {})
            vacancy = cls(
                title=item.get("name", ""),
                url=item.get("alternate_url", ""),
                salary_from=salary.get("from"),
                salary_to=salary.get("to"),
                description=item.get("snippet", {}).get("responsibility", ""),
                requirements=item.get("snippet", {}).get("requirement", ""),
            )
            vacancies.append(vacancy)
        return vacancies
