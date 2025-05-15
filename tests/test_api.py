from unittest.mock import MagicMock, patch

from src.api.hh_api import HeadHunterAPI


@patch("src.api.hh_api.requests.get")
def test_connect_success(mock_get):
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    api.connect()

    mock_get.assert_called_once_with(
        "https://api.hh.ru/vacancies", headers={"User-Agent": "HH-User-Agent"}
    )


@patch("src.api.hh_api.requests.get")
def test_get_vacancies(mock_get):
    # Создаём поддельный JSON-ответ
    mock_response = MagicMock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {
        "items": [
            {"id": 1, "name": "Python Developer"},
            {"id": 2, "name": "Django Developer"},
        ]
    }
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    result = api.get_vacancies("python")

    assert isinstance(result, list)
    assert len(result) == 10  # 2 вакансии * 5 страниц
    assert result[0]["name"] == "Python Developer"
    assert mock_get.call_count == 6  # 1 на connect + 5 на get_vacancies

    # Проверим, что keyword передается корректно
    for call in mock_get.call_args_list[1:]:
        _, kwargs = call
        assert kwargs["params"]["text"] == "python"
