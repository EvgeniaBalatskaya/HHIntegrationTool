from typing import List, Dict
from src.models.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], filter_words: List[str]) -> List[Vacancy]:
    """
    Фильтрует вакансии по ключевым словам в описании

    :param vacancies: Список вакансий
    :param filter_words: Список ключевых слов
    :return: Отфильтрованный список вакансий
    """
    if not filter_words:
        return vacancies

    filtered = []
    for vacancy in vacancies:
        text = f"{vacancy.description} {vacancy.requirements}".lower()
        if all(word.lower() in text for word in filter_words):
            filtered.append(vacancy)
    return filtered


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрует вакансии по диапазону зарплат

    :param vacancies: Список вакансий
    :param salary_range: Диапазон зарплат (формат: "100000-150000")
    :return: Отфильтрованный список вакансий
    """
    if not salary_range:
        return vacancies

    try:
        min_salary, max_salary = map(int, salary_range.split('-'))
    except ValueError:
        return vacancies

    return [v for v in vacancies if min_salary <= v.salary_from <= max_salary]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """Сортирует вакансии по убыванию зарплаты"""
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий

    :param vacancies: Список вакансий
    :param top_n: Количество вакансий для возврата
    :return: Список топ вакансий
    """
    return vacancies[:top_n]