import pytest

from src.models.vacancy import Vacancy
from src.utils.filters import (filter_vacancies, get_top_vacancies,
                               get_vacancies_by_salary, sort_vacancies)


class TestFilters:
    """Тесты для вспомогательных функций"""

    @pytest.fixture
    def sample_vacancies(self):
        return [
            Vacancy("Python", "url1", 100000, 150000, "Python Django", "Python"),
            Vacancy("Java", "url2", 90000, 120000, "Java Spring", "Java"),
            Vacancy("Fullstack", "url3", 120000, None, "Python JavaScript", "JS"),
        ]

    def test_filter_vacancies(self, sample_vacancies):
        """Тест фильтрации по ключевым словам"""
        filtered = filter_vacancies(sample_vacancies, ["python"])
        assert len(filtered) == 2
        assert all("Python" in v.title or "Python" in v.description for v in filtered)

        filtered = filter_vacancies(sample_vacancies, ["spring"])
        assert len(filtered) == 1
        assert filtered[0].title == "Java"

    def test_filter_empty_keywords(self, sample_vacancies):
        """Тест фильтрации без ключевых слов"""
        filtered = filter_vacancies(sample_vacancies, [])
        assert len(filtered) == len(sample_vacancies)

    def test_get_vacancies_by_salary(self, sample_vacancies):
        """Тест фильтрации по зарплате"""
        ranged = get_vacancies_by_salary(sample_vacancies, "90000-110000")
        assert len(ranged) == 1
        assert ranged[0].title == "Python"

        ranged = get_vacancies_by_salary(sample_vacancies, "110000-")
        assert len(ranged) == 2

    def test_sort_vacancies(self, sample_vacancies):
        """Тест сортировки вакансий"""
        sorted_list = sort_vacancies(sample_vacancies)
        assert sorted_list[0].title == "Fullstack"
        assert sorted_list[1].title == "Python"
        assert sorted_list[2].title == "Java"

    def test_get_top_vacancies(self, sample_vacancies):
        """Тест получения топ N вакансий"""
        top = get_top_vacancies(sample_vacancies, 2)
        assert len(top) == 2
        assert top[0].salary_from >= top[1].salary_from
