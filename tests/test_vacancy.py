import pytest
from src.models.vacancy import Vacancy


class TestVacancy:
    """Тесты для класса Vacancy"""

    @pytest.fixture
    def sample_vacancy(self):
        return Vacancy(
            title="Python Developer",
            url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            description="Develop software",
            requirements="Python experience"
        )

    def test_vacancy_creation(self, sample_vacancy):
        """Тест создания вакансии"""
        assert sample_vacancy.title == "Python Developer"
        assert sample_vacancy.salary_from == 100000
        assert sample_vacancy.salary_to == 150000

    def test_salary_validation_none(self):
        """Тест валидации при отсутствии зарплаты"""
        v = Vacancy("Dev", "url", None, None, "", "")
        assert v.salary_from == 0
        assert v.salary_to == 0

    def test_comparison_operators(self):
        """Тест операторов сравнения"""
        v1 = Vacancy("Junior", "url1", 50000, None, "", "")
        v2 = Vacancy("Senior", "url2", 150000, None, "", "")

        assert v2 > v1
        assert v1 < v2
        assert not v1 > v2
        assert not v2 < v1

    def test_cast_to_object_list(self):
        """Тест преобразования JSON в объекты"""
        json_data = [{
            "name": "Dev",
            "alternate_url": "http://example.com",
            "salary": {"from": 100000, "to": 150000},
            "snippet": {
                "requirement": "Python",
                "responsibility": "Develop"
            }
        }]
        vacancies = Vacancy.cast_to_object_list(json_data)

        assert len(vacancies) == 1
        assert isinstance(vacancies[0], Vacancy)
        assert vacancies[0].title == "Dev"
        assert vacancies[0].salary_from == 100000

    def test_cast_to_object_list_no_salary(self):
        """Тест преобразования при отсутствии зарплаты"""
        json_data = [{
            "name": "Dev",
            "alternate_url": "http://example.com",
            "snippet": {
                "requirement": "Python",
                "responsibility": "Develop"
            }
        }]
        vacancies = Vacancy.cast_to_object_list(json_data)

        assert vacancies[0].salary_from == 0
        assert vacancies[0].salary_to == 0
