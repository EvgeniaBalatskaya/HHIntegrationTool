import sys
from src.api.hh_api import HeadHunterAPI
from src.models.vacancy import Vacancy
from src.storage.json_storage import JSONStorage
from src.utils.filters import filter_vacancies, sort_vacancies, get_top_vacancies


def user_interaction():
    """Основная функция взаимодействия с пользователем"""
    try:
        print("Добро пожаловать в HH Integration Tool!")

        # Инициализация компонентов
        hh_api = HeadHunterAPI()
        storage = JSONStorage()

        # Получение входных данных
        search_query = input("Введите поисковый запрос: ").strip()
        if not search_query:
            raise ValueError("Поисковый запрос не может быть пустым")

        top_n = int(input("Введите количество вакансий для вывода в топ N: "))
        filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
        salary_input = input("Введите минимальную зарплату (Enter для пропуска): ").strip()

        # Получение и обработка вакансий
        print("\nПолучаем вакансии с HeadHunter...")
        vacancies_data = hh_api.get_vacancies(search_query)
        vacancies = Vacancy.cast_to_object_list(vacancies_data)

        # Фильтрация
        if filter_words:
            vacancies = filter_vacancies(vacancies, filter_words)

        if salary_input:
            try:
                min_salary = int(salary_input)
                vacancies = [v for v in vacancies if v.salary_from >= min_salary]
            except ValueError:
                print("Некорректное значение зарплаты, фильтрация по зарплате пропущена")

        # Сохранение и вывод результатов
        for vacancy in vacancies:
            storage.add_vacancy(vacancy)

        sorted_vacancies = sort_vacancies(vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        print("\nРезультаты поиска:")
        if not top_vacancies:
            print("Нет вакансий, соответствующих критериям")
        else:
            for i, vacancy in enumerate(top_vacancies, 1):
                print(f"\n{i}. {vacancy.title}")
                print(f"   Зарплата: {vacancy.salary_from or 'не указана'} - {vacancy.salary_to or ''}")
                print(f"   Требования: {vacancy.requirements[:100]}...")
                print(f"   Описание: {vacancy.description[:100]}...")
                print(f"   Ссылка: {vacancy.url}")

        print(f"\nВсего найдено вакансий: {len(vacancies)}")
        print(f"Показано топ {len(top_vacancies)} вакансий")

    except ValueError as e:
        print(f"\nОшибка ввода: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    user_interaction()
