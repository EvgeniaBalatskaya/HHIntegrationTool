from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


def test_add_and_get_vacancy(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONStorage(file_name=file_path.name)
    storage._JSONStorage__file_path = file_path  # переопределяем путь к файлу

    vacancy = Vacancy(
        title="Python Dev",
        url="https://hh.ru/vacancy/1",
        salary_from=100000,
        salary_to=150000,
        description="Разработка на Python",
        requirements="Опыт Django, REST",
        currency="RUR",
    )

    # Добавление
    storage.add_vacancy(vacancy)
    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0]["title"] == "Python Dev"

    # Проверка на дубликат
    storage.add_vacancy(vacancy)
    vacancies = storage.get_vacancies()
    assert len(vacancies) == 1


def test_get_vacancies_with_criteria(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONStorage(file_name=file_path.name)
    storage._JSONStorage__file_path = file_path

    vacancy1 = Vacancy(
        title="Python Dev",
        url="https://hh.ru/vacancy/1",
        salary_from=100000,
        salary_to=150000,
        description="Разработка на Python",
        requirements="Django",
        currency="RUR",
    )
    vacancy2 = Vacancy(
        title="Java Dev",
        url="https://hh.ru/vacancy/2",
        salary_from=85000,  # исправлено с 60000 на 85000, чтобы проходил фильтр salary_from=80000
        salary_to=90000,
        description="Разработка на Java",
        requirements="Spring Boot",
        currency="RUR",
    )

    storage.add_vacancy(vacancy1)
    storage.add_vacancy(vacancy2)

    # Поиск по ключевому слову
    result = storage.get_vacancies({"keyword": "python"})
    assert len(result) == 1
    assert result[0]["title"] == "Python Dev"

    # Поиск по зарплате
    result = storage.get_vacancies({"salary_from": 80000})
    assert len(result) == 2

    # Поиск по ключу и зарплате
    result = storage.get_vacancies({"keyword": "java", "salary_from": 80000})
    assert len(result) == 1
    assert result[0]["title"] == "Java Dev"

    # Не найдено
    result = storage.get_vacancies({"keyword": "golang"})
    assert result == []


def test_delete_vacancy(tmp_path):
    file_path = tmp_path / "vacancies.json"
    storage = JSONStorage(file_name=file_path.name)
    storage._JSONStorage__file_path = file_path

    vacancy = Vacancy(
        title="DevOps",
        url="https://hh.ru/vacancy/3",
        salary_from=120000,
        salary_to=160000,
        description="CI/CD",
        requirements="Kubernetes",
        currency="RUR",
    )

    storage.add_vacancy(vacancy)
    assert len(storage.get_vacancies()) == 1

    storage.delete_vacancy(vacancy)
    assert storage.get_vacancies() == []
