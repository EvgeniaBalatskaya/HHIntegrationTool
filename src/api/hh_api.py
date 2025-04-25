from typing import Dict, List

import requests

from src.api.abstract_api import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API HeadHunter"""

    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def connect(self) -> None:
        """Приватный метод подключения к API"""
        response = requests.get(self.__base_url, headers=self.__headers)
        response.raise_for_status()

    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получение вакансий с hh.ru по ключевому слову

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий
        """
        self.connect()
        self.__params["text"] = keyword
        vacancies = []

        for page in range(5):  # Ограничим 5 страницами
            self.__params["page"] = page
            response = requests.get(
                self.__base_url, headers=self.__headers, params=self.__params
            )
            response.raise_for_status()
            vacancies.extend(response.json()["items"])

        return vacancies
