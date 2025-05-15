from unittest.mock import MagicMock, patch

import pytest

from src.main import user_interaction


@pytest.fixture
def mock_vacancy():
    mock = MagicMock()
    mock.title = "Python Developer"
    mock.salary_from = 100000
    mock.salary_to = 150000
    mock.requirements = "Python, Django, REST"
    mock.description = "Backend developer with experience in Django"
    mock.url = "https://example.com/vacancy"
    return mock


@patch("src.main.print")
@patch("src.main.JSONStorage")
@patch("src.main.Vacancy")
@patch("src.main.HeadHunterAPI")
@patch("builtins.input")
def test_user_interaction_full_flow(
    mock_input, mock_api, mock_vacancy_cls, mock_storage_cls, mock_print
):
    # Настраиваем ввод от пользователя
    mock_input.side_effect = [
        "python",  # search_query
        "3",  # top_n
        "django rest",  # filter_words
        "90000",  # salary_from
    ]

    # Поддельные данные от API
    mock_api_instance = mock_api.return_value
    mock_api_instance.get_vacancies.return_value = [{"id": 1}]

    # Поддельные вакансии
    vacancy_obj = MagicMock()
    vacancy_obj.title = "Python Developer"
    vacancy_obj.salary_from = 100000
    vacancy_obj.salary_to = 150000
    vacancy_obj.requirements = "Python, Django, REST"
    vacancy_obj.description = "Backend developer with experience in Django"
    vacancy_obj.url = "https://example.com/vacancy"

    mock_vacancy_cls.cast_to_object_list.return_value = [vacancy_obj]

    # Поддельное хранилище
    mock_storage = mock_storage_cls.return_value
    mock_storage.add_vacancy.return_value = None

    user_interaction()

    # Проверяем, что API был вызван
    mock_api_instance.get_vacancies.assert_called_once_with("python")

    # Проверяем фильтрацию и сохранение вакансий
    assert mock_storage.add_vacancy.call_count >= 1

    # Проверяем, что результат выводится
    printed_texts = [args[0] for args, _ in mock_print.call_args_list]
    assert any("Результаты поиска" in line for line in printed_texts)
    assert any("Python Developer" in line for line in printed_texts)
