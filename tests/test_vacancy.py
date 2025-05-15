import pytest

from src.models.vacancy import Vacancy


def test_valid_vacancy_creation():
    vacancy = Vacancy(
        title=" Python Developer ",
        url="https://hh.ru/vacancy/123456",
        salary_from=100000,
        salary_to=150000,
        currency="RUR",
        description=" Разработка бэкенда ",
        requirements=" Опыт с Python ",
    )

    assert vacancy.title == "Python Developer"
    assert vacancy.url == "https://hh.ru/vacancy/123456"
    assert vacancy.salary_from == 100000.0
    assert vacancy.salary_to == 150000.0
    assert vacancy.currency == "RUR"
    assert vacancy.description == "Разработка бэкенда"
    assert vacancy.requirements == "Опыт с Python"


def test_invalid_url_raises_error():
    with pytest.raises(ValueError):
        Vacancy(
            title="Dev",
            url="https://example.com/123",
            salary_from=100000,
            salary_to=150000,
            currency="RUR",
            description="",
            requirements="",
        )


def test_salary_normalization_and_swap():
    vacancy = Vacancy(
        title="Test",
        url="https://hh.ru/vacancy/123",
        salary_from=200000,
        salary_to=100000,
        currency="RUR",
        description="",
        requirements="",
    )
    assert vacancy.salary_from == 100000.0
    assert vacancy.salary_to == 200000.0


def test_less_than_operator():
    v1 = Vacancy("Dev1", "https://hh.ru/vacancy/1", 100000, 150000, "RUR", "", "")
    v2 = Vacancy("Dev2", "https://hh.ru/vacancy/2", 120000, 160000, "RUR", "", "")
    v3 = Vacancy("Dev3", "https://hh.ru/vacancy/3", 90000, 130000, "USD", "", "")

    assert v1 < v2
    assert not (v2 < v1)
    assert not (v1 < v3)  # валюты разные → False


def test_repr_output():
    vacancy = Vacancy("Dev", "https://hh.ru/vacancy/1", 100000, 120000, "RUR", "", "")
    expected = (
        "Vacancy(title='Dev', url='https://hh.ru/vacancy/1', "
        "salary_from=100000.0, salary_to=120000.0, currency='RUR')"
    )
    assert repr(vacancy) == expected


def test_cast_to_object_list_valid_data():
    data = [
        {
            "name": "Backend Dev",
            "alternate_url": "https://hh.ru/vacancy/123",
            "salary": {"from": 80000, "to": 120000, "currency": "RUR"},
            "snippet": {"responsibility": "Backend dev", "requirement": "Python"},
        },
        {
            "name": "Invalid",
            "alternate_url": "invalid-url",
            "salary": {},
            "snippet": {},
        },
    ]
    vacancies = Vacancy.cast_to_object_list(data)
    assert len(vacancies) == 1
    assert vacancies[0].title == "Backend Dev"
    assert vacancies[0].salary_from == 80000.0


def test_cast_to_object_list_invalid_data():
    assert Vacancy.cast_to_object_list(None) == []
    assert Vacancy.cast_to_object_list("not a list") == []
    assert Vacancy.cast_to_object_list([1, 2, 3]) == []
