import pytest
from unittest.mock import patch, Mock
from src.api.hh_api import HeadHunterAPI
from src.api.abstract_api import VacancyAPI


class TestHeadHunterAPI:
    """Тесты для класса HeadHunterAPI"""

    def test_is_instance_of_abstract_class(self):
        """Проверка, что класс наследуется от VacancyAPI"""
        assert issubclass(HeadHunterAPI, VacancyAPI)

    @patch('requests.get')
    def test_connect_success(self, mock_get):
        """Тест успешного подключения к API"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        hh_api.connect()  # Не должно вызывать исключений

    @patch('requests.get')
    def test_connect_failure(self, mock_get):
        """Тест неудачного подключения к API"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        with pytest.raises(Exception):
            hh_api.connect()

    @patch('requests.get')
    def test_get_vacancies(self, mock_get):
        """Тест получения вакансий"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'items': [{
                'name': 'Python Developer',
                'alternate_url': 'http://example.com',
                'salary': {'from': 100000, 'to': 150000},
                'snippet': {
                    'requirement': 'Python experience',
                    'responsibility': 'Develop software'
                }
            }]
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        hh_api = HeadHunterAPI()
        vacancies = hh_api.get_vacancies('Python')

        assert len(vacancies) == 1
        assert vacancies[0]['name'] == 'Python Developer'