import re
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Vacancy:
    """Класс для представления вакансии с оптимизацией памяти"""

    __slots__ = [
        "_title",
        "_url",
        "_salary_from",
        "_salary_to",
        "_currency",
        "_description",
        "_requirements",
    ]

    def __init__(
        self,
        title: str,
        url: str,
        salary_from: Optional[float],
        salary_to: Optional[float],
        currency: Optional[str],
        description: Optional[str],
        requirements: Optional[str],
    ):
        self._title = title
        self._url = url
        self._salary_from = salary_from
        self._salary_to = salary_to
        self._currency = currency
        self._description = description or ""
        self._requirements = requirements or ""
        self._validate()

    def _validate(self) -> None:
        """Проверка и нормализация данных"""
        self._validate_url()
        self._validate_salary()
        self._validate_text_fields()

    def _validate_url(self) -> None:
        """Проверка корректности URL"""
        if not re.match(r"^https?://(?:www\.)?hh\.ru/vacancy/\d+", self._url):
            raise ValueError(f"Некорректный URL вакансии: {self._url}")

    def _validate_salary(self) -> None:
        """Нормализация данных о зарплате"""
        if self._salary_from is not None:
            self._salary_from = float(self._salary_from)
        if self._salary_to is not None:
            self._salary_to = float(self._salary_to)

        if (
            self._salary_from
            and self._salary_to
            and self._salary_from > self._salary_to
        ):
            self._salary_from, self._salary_to = self._salary_to, self._salary_from

    def _validate_text_fields(self) -> None:
        """Очистка текстовых полей"""
        self._title = self._title.strip() if self._title else ""
        self._description = self._description.strip() if self._description else ""
        self._requirements = self._requirements.strip() if self._requirements else ""

    @property
    def title(self) -> str:
        return self._title

    @property
    def url(self) -> str:
        return self._url

    @property
    def salary_from(self) -> Optional[float]:
        return self._salary_from

    @property
    def salary_to(self) -> Optional[float]:
        return self._salary_to

    @property
    def currency(self) -> Optional[str]:
        return self._currency

    @property
    def description(self) -> str:
        return self._description

    @property
    def requirements(self) -> str:
        return self._requirements

    def __lt__(self, other: "Vacancy") -> bool:
        """Сравнение с учётом валюты"""
        if self.currency != other.currency:
            return False
        return (self.salary_from or 0) < (other.salary_from or 0)

    def __repr__(self) -> str:
        return (
            f"Vacancy(title={self.title!r}, url={self.url!r}, "
            f"salary_from={self.salary_from}, salary_to={self.salary_to}, "
            f"currency={self.currency!r})"
        )

    @classmethod
    def cast_to_object_list(cls, data: List[Dict]) -> List["Vacancy"]:
        """Преобразование JSON в список объектов"""
        vacancies: List[Vacancy] = []
        if not data or not isinstance(data, list):
            return vacancies

        for item in data:
            if not isinstance(item, dict):
                continue

            salary = item.get("salary") or {}
            snippet = item.get("snippet") or {}

            try:
                vacancy = cls(
                    title=item.get("name", ""),
                    url=item.get("alternate_url", ""),
                    salary_from=salary.get("from"),
                    salary_to=salary.get("to"),
                    currency=salary.get("currency"),
                    description=snippet.get("responsibility"),
                    requirements=snippet.get("requirement"),
                )
                vacancies.append(vacancy)
            except (ValueError, AttributeError):
                continue

        return vacancies
