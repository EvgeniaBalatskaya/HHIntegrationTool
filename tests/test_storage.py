import pytest
import json
import os
from pathlib import Path
from unittest.mock import patch, mock_open
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage


class TestJSONStorage:
    """Тесты для класса JSONStorage"""

    @pytest.fixture
    def storage(self, tmp_path):
        """Фикстура с временным файлом"""
        d = tmp_path / "data"
        d.mkdir()
        storage = JSONStorage(file_name="test_vacancies.json")
        storage._JSONStorage__file_path = d / "test_vacancies.json"
        return storage

    @pytest.fixture
    def sample_vacancy(self):
        return Vacancy(
            title="Python Developer",
            url="http://example.com",
            salary_from=100000,
            salary_to=150000,
            description="Develop",
            requirements="Python"
        )

    def test_add_vacancy(self, storage, sample_vacancy):
        """Тест добавления вакансии"""
        storage.add_vacancy(sample_vacancy)

        with open(storage._JSONStorage__file_path, 'r') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]['title'] == "Python Developer"

    def test_add_duplicate_vacancy(self, storage, sample_vacancy):
        """Тест добавления дубликата вакансии"""
        storage.add_vacancy(sample_vacancy)
        storage.add_vacancy(sample_vacancy)  # Дубликат

        with open(storage._JSONStorage__file_path, 'r') as f:
            data = json.load(f)

        assert len(data) == 1  # Дубликат не добавлен

    def test_get_vacancies_empty(self, storage):
        """Тест получения вакансий из пустого файла"""
        assert storage.get_vacancies() == []

    def test_get_vacancies_with_filter(self, storage, sample_vacancy):
        """Тест фильтрации вакансий"""
        storage.add_vacancy(sample_vacancy)

        # Фильтр по ключевому слову
        filtered = storage.get_vacancies({'keyword': 'python'})
        assert len(filtered) == 1

        # Фильтр по зарплате
        filtered = storage.get_vacancies({'salary_from': 90000})
        assert len(filtered) == 1

        # Несоответствующий фильтр
        filtered = storage.get_vacancies({'keyword': 'java'})
        assert len(filtered) == 0

    def test_delete_vacancy(self, storage, sample_vacancy):
        """Тест удаления вакансии"""
        storage.add_vacancy(sample_vacancy)
        storage.delete_vacancy(sample_vacancy)

        with open(storage._JSONStorage__file_path, 'r') as f:
            data = json.load(f)

        assert len(data) == 0

    def test_file_creation(self, tmp_path):
        """Тест автоматического создания файла"""
        d = tmp_path / "new_data"
        storage = JSONStorage(file_name="new_file.json")
        storage._JSONStorage__file_path = d / "new_file.json"

        # Файл не должен существовать до добавления вакансии
        assert not os.path.exists(storage._JSONStorage__file_path)

        # После добавления - должен быть создан
        storage.add_vacancy(Vacancy(
            title="Test", url="http://test.com",
            salary_from=None, salary_to=None,
            description="", requirements=""
        ))
        assert os.path.exists(storage._JSONStorage__file_path)
