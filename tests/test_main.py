import sys
from io import StringIO
from unittest.mock import patch

import pytest

from src.main import user_interaction
from src.models.vacancy import Vacancy


class TestMain:
    """Тесты для основного скрипта main.py"""

    @pytest.fixture
    def sample_vacancy(self):
        return Vacancy(
            title="Python Developer",
            url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            description="Develop web applications",
            requirements="Python experience",
        )

    @patch("builtins.input")
    @patch("main.HeadHunterAPI")
    @patch("main.JSONStorage")
    def test_user_interaction_success(
        self, mock_storage, mock_api, mock_input, sample_vacancy
    ):
        """Тест успешного выполнения user_interaction"""
        # Настройка моков
        mock_input.side_effect = [
            "Python",  # Поисковый запрос
            "2",  # Количество вакансий
            "Django",  # Ключевые слова
            "100000",  # Минимальная зарплата
        ]

        # Мок API
        api_instance = mock_api.return_value
        api_instance.get_vacancies.return_value = [
            {
                "name": "Python Developer",
                "alternate_url": "http://example.com",
                "salary": {"from": 100000, "to": 150000},
                "snippet": {
                    "requirement": "Python Django",
                    "responsibility": "Develop web applications",
                },
            }
        ]

        # Мок хранилища
        storage_instance = mock_storage.return_value

        # Перенаправление stdout
        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            user_interaction()

            output = out.getvalue()
            assert "Добро пожаловать" in output
            assert "Python Developer" in output
            assert "100000" in output
            assert storage_instance.add_vacancy.called
        finally:
            sys.stdout = saved_stdout

    @patch("builtins.input")
    def test_user_interaction_empty_query(self, mock_input):
        """Тест обработки пустого поискового запроса"""
        mock_input.return_value = ""

        saved_stderr = sys.stderr
        try:
            err = StringIO()
            sys.stderr = err

            with pytest.raises(SystemExit):
                user_interaction()

            assert "не может быть пустым" in err.getvalue()
        finally:
            sys.stderr = saved_stderr

    @patch("builtins.input")
    @patch("main.HeadHunterAPI")
    def test_user_interaction_api_error(self, mock_api, mock_input):
        """Тест обработки ошибки API"""
        mock_input.side_effect = ["Python", "2", "", ""]

        api_instance = mock_api.return_value
        api_instance.get_vacancies.side_effect = Exception("API error")

        saved_stderr = sys.stderr
        try:
            err = StringIO()
            sys.stderr = err

            with pytest.raises(SystemExit):
                user_interaction()

            assert "Произошла ошибка" in err.getvalue()
        finally:
            sys.stderr = saved_stderr

    @patch("builtins.input")
    @patch("main.HeadHunterAPI")
    @patch("main.JSONStorage")
    def test_user_interaction_no_results(self, mock_storage, mock_api, mock_input):
        """Тест случая, когда нет результатов"""
        mock_input.side_effect = ["Python", "2", "Java", ""]

        api_instance = mock_api.return_value
        api_instance.get_vacancies.return_value = []

        saved_stdout = sys.stdout
        try:
            out = StringIO()
            sys.stdout = out

            user_interaction()

            output = out.getvalue()
            assert "Нет вакансий" in output
        finally:
            sys.stdout = saved_stdout
