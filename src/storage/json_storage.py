import json
import os
from pathlib import Path
from typing import List, Dict
from src.models.vacancy import Vacancy
from src.storage.abstract_storage import Storage


class JSONStorage(Storage):
    """Класс для работы с JSON-файлом как хранилищем вакансий"""

    def __init__(self, file_name: str = 'vacancies.json'):
        self.__file_name = file_name
        self.__ensure_directory_exists()

    def __ensure_directory_exists(self) -> None:
        """Создает директорию data если её нет"""
        Path('data').mkdir(exist_ok=True)
        self.__file_path = Path('data') / self.__file_name

    def add_vacancy(self, vacancy: Vacancy) -> None:
        """Добавляет вакансию в JSON-файл, избегая дубликатов"""
        vacancies = self.__load_vacancies()

        if not any(v['url'] == vacancy.url for v in vacancies):
            vacancies.append({
                'title': vacancy.title,
                'url': vacancy.url,
                'salary_from': vacancy.salary_from,
                'salary_to': vacancy.salary_to,
                'description': vacancy.description,
                'requirements': vacancy.requirements
            })
            self.__save_vacancies(vacancies)

    def get_vacancies(self, criteria: Dict = None) -> List[Dict]:
        """Возвращает вакансии, отфильтрованные по критериям"""
        vacancies = self.__load_vacancies()

        if not criteria:
            return vacancies

        filtered = []
        for vacancy in vacancies:
            match = True
            if 'keyword' in criteria:
                keyword = criteria['keyword'].lower()
                desc = vacancy['description'].lower()
                reqs = vacancy['requirements'].lower()
                if keyword not in desc and keyword not in reqs:
                    match = False
            if 'salary_from' in criteria and vacancy.get('salary_from', 0) < criteria['salary_from']:
                match = False
            if match:
                filtered.append(vacancy)

        return filtered

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        """Удаляет вакансию из JSON-файла"""
        vacancies = self.__load_vacancies()
        vacancies = [v for v in vacancies if v['url'] != vacancy.url]
        self.__save_vacancies(vacancies)

    def __load_vacancies(self) -> List[Dict]:
        """Загружает вакансии из JSON-файла"""
        if not self.__file_path.exists():
            return []

        with open(self.__file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __save_vacancies(self, vacancies: List[Dict]) -> None:
        """Сохраняет вакансии в JSON-файл"""
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=2)