from abc import ABC, abstractmethod
from typing import Dict, List


class VacancyAPI(ABC):
    """Абстрактный класс для работы с API сервисов вакансий"""

    @abstractmethod
    def connect(self) -> None:
        """Подключение к API"""
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str) -> List[Dict]:
        """
        Получение вакансий по ключевому слову

        :param keyword: Ключевое слово для поиска
        :return: Список вакансий в виде словарей
        """
        pass
