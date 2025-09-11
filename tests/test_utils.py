import pytest

from src.models.vacancy import Vacancy
from src.utils.filters import (filter_vacancies, get_top_vacancies,
                               get_vacancies_by_salary, sort_vacancies)


@pytest.fixture
def sample_vacancies():
    return [
        Vacancy(
            title="Python Developer",
            url="https://hh.ru/vacancy/1",
            salary_from=120000,
            salary_to=150000,
            description="Опыт с Django",
            requirements="Python, Django",
            currency="RUR",
        ),
        Vacancy(
            title="Junior Developer",
            url="https://hh.ru/vacancy/2",
            salary_from=80000,
            salary_to=100000,
            description="Только начинающий",
            requirements="HTML, CSS",
            currency="RUR",
        ),
        Vacancy(
            title="Middle Python",
            url="https://hh.ru/vacancy/3",
            salary_from=110000,
            salary_to=130000,
            description="Python и Flask",
            requirements="Flask",
            currency="RUR",
        ),
    ]


def test_filter_vacancies_with_keywords(sample_vacancies):
    result = filter_vacancies(sample_vacancies, ["django", "python"])
    assert len(result) == 1
    assert result[0].title == "Python Developer"


def test_get_top_vacancies(sample_vacancies):
    sorted_list = sort_vacancies(sample_vacancies)
    top = get_top_vacancies(sorted_list, 2)
    assert len(top) == 2
    assert top[0].salary_from >= top[1].salary_from


def test_get_vacancies_by_salary(sample_vacancies):
    # Передаём диапазон зарплат в виде строки "min-max"
    result = get_vacancies_by_salary(sample_vacancies, "110000-130000")
    assert len(result) == 2
    titles = [vac.title for vac in result]
    assert "Python Developer" in titles
    assert "Middle Python" in titles


def test_sort_vacancies(sample_vacancies):
    sorted_list = sort_vacancies(sample_vacancies)
    assert sorted_list[0].salary_from == 120000
