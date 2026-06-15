import random
import sys
import time
from typing import Dict, Tuple

STOP_WORD = 'СТОП'


def load_words(filename: str = 'words.txt') -> Dict[str, str]:
    """
    Загружает пары слов и переводов из файла.

    Аргументы:
        filename (str): Имя файла для загрузки. По умолчанию 'words.txt'.

    Возвращает:
        Dict[str, str]: Словарь, где ключ — слово, значение — перевод.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = file.read().split('\n')
            dictionary = dict()
            for item in data:
                if item.count(',') == 1:
                    word, translation = item.split(',')
                    dictionary[word.strip()] = translation.strip()
        return dictionary
    except FileNotFoundError:
        print(f'Ошибка: файл {filename} не найден.')
        sys.exit(1)


def print_statistics(score: int, total_time: float) -> None:
    """
    Выводит статистику игры.

    Аргументы:
        score (int): Количество правильных ответов.
        total_time (float): Общее время игры в секундах.

    Возвращает:
        None
    """
    print(f'Ваш итоговый счет: {score}')

    avg_time = f'{round(total_time / score, 2)} сек.' if score > 0 else '—'
    print(f'Время игры: {total_time:.2f} секунд (среднее время: {avg_time})')


def ask_and_check(word: str, correct: str) -> Tuple[bool, bool, float]:
    """
    Запрашивает у пользователя перевод слова и проверяет его.

    Аргументы:
        word (str): Слово для перевода.
        correct (str): Правильный перевод.

    Возвращает:
        Tuple[bool, bool, float]: Кортеж из трёх элементов:
            - need_to_exit (bool): True, если пользователь ввёл STOP_WORD
            - is_correct (bool): True, если перевод правильный
            - answer_time (float): Время, затраченное на ответ в секундах
    """
    print(f'Ваше слово: {word}')
    answer_start_time = time.time()

    user_translation = input('Ваш перевод: ').strip()
    answer_time = time.time() - answer_start_time

    if user_translation.upper().strip() == STOP_WORD:
        return (True, False, 0.0)
    else:
        return (False,
                user_translation.lower().strip() == correct.lower(),
                answer_time)


def start_game(words: Dict[str, str]) -> None:
    """
    Запускает основной игровой режим.

    Аргументы:
        words (Dict[str, str]): Словарь слов и переводов.

    Возвращает:
        None

    Примечания:
        - Игра продолжается до ввода STOP_WORD
        - После завершения выводится статистика
    """
    if not words:
        print('Словарь пуст.')
        return
    print(f'Чтобы закончить, введите {STOP_WORD}')

    score = 0
    total_time = 0.0

    while True:
        word, correct_translation = random.choice(list(words.items()))
        need_to_exit, is_correct, answer_time = ask_and_check(
            word, correct_translation)
        total_time += answer_time
        if need_to_exit:
            print_statistics(score, total_time)
            break
        else:
            if is_correct:
                score += 1
                print(f'Верно! Всего очков: {score} '
                      f'(ответ за {answer_time:.2f} секунд)')
            else:
                print(f'Неправильно, правильный ответ: {correct_translation} '
                      f'(Время на ответ: {answer_time:.2f} секунд)')


def train_until_mistake(words: Dict[str, str]) -> None:
    """
    Запускает режим тренировки до первой ошибки.

    Аргументы:
        words (Dict[str, str]): Словарь слов и переводов.

    Возвращает:
        None

    Примечания:
        - После ошибки или выхода выводится статистика
    """
    if not words:
        print('Словарь пуст.')
        return

    print('Режим: Игра до первой ошибки! '
          f'Чтобы выйти вручную, введите {STOP_WORD}')

    score = 0
    total_time = 0.0

    while True:
        word, correct_translation = random.choice(list(words.items()))
        need_to_exit, is_correct, answer_time = ask_and_check(
            word, correct_translation)
        total_time += answer_time
        if need_to_exit:
            print('Выход из режима по запросу пользователя.')
            print_statistics(score, total_time)
            break

        if is_correct:
            score += 1
            print(f'Верно! Всего очков: {score} '
                  f'(ответ за {answer_time:.2f} секунд)')
        else:
            print(f'Ошибка! Неверно. Правильный ответ: {correct_translation}')
            print_statistics(score, total_time)
            break


def add_words(words: Dict[str, str]) -> None:
    """
    Добавляет новые слова в словарь в интерактивном режиме.

    Аргументы:
        words (Dict[str, str]): Словарь для пополнения.

    Возвращает:
        None
    """
    print(f'Чтобы закончить, введите {STOP_WORD}')
    while True:
        new_word = input('Введите слово: ')
        if new_word.strip().upper() == STOP_WORD:
            break

        translation = input('Введите перевод: ')
        if translation.strip().upper() == STOP_WORD:
            break

        if new_word.strip() and translation.strip():
            words[new_word.strip()] = translation.strip()
        else:
            print("Слово и перевод не могут быть пустыми. Попробуйте снова.")


def show_all_words(words: Dict[str, str]) -> None:
    """
    Выводит все пары "слово - перевод" из словаря.

    Аргументы:
        words (Dict[str, str]): Словарь слов и переводов.

    Возвращает:
        None

    Примечания:
        - Если словарь пуст, выводится пустая строка
    """
    if not words:
        print()
        return
    formatted = [f'{word} - {translation}'
                 for word, translation in words.items()]
    print('; '.join(formatted))


def save_words(words: Dict[str, str], filename: str = 'words.txt') -> None:
    """
    Сохраняет словарь в файл.

    Аргументы:
        words (Dict[str, str]): Словарь слов и переводов.
        filename (str): Имя файла для сохранения. По умолчанию 'words.txt'.

    Возвращает:
        None

    Примечания:
        - Файл сохраняется в формате "слово, перевод" на каждой строке
        - Если файл существует, он будет перезаписан
        - При ошибке программа завершается с кодом 1
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            counter = 0
            for word, translation in words.items():
                file.write(f'{word}, {translation}\n')
                counter += 1
            print(f'Было сохранено {counter} слов в файл {filename}')
    except Exception:
        print('Произошла ошибка при сохранении словаря.')
        sys.exit(1)


def main():
    """
    Главная функция программы.

    Загружает словарь из файла и запускает интерактивное меню,
    позволяющее пользователю выбирать различные режимы работы:
    - Обычная игра
    - Добавление новых слов
    - Тренировка до первой ошибки
    - Просмотр всех слов
    - Выход с сохранением

    Возвращает:
        None
    """
    words = load_words()
    print(f'Было загружено {len(words)} слов из файла words.txt')

    while True:
        menu = '''Меню:
        1. Начать игру
        2. Добавить слова
        3. Тренировка до первой ошибки
        4. Вывод всех слов
        5. Выход
        '''
        print(menu)
        menu_choice = input('Пункт меню: ').strip()

        try:
            menu_choice = int(menu_choice)
            if menu_choice == 1:
                start_game(words)
            elif menu_choice == 2:
                add_words(words)
            elif menu_choice == 3:
                train_until_mistake(words)
            elif menu_choice == 4:
                show_all_words(words)
            elif menu_choice == 5:
                save_words(words)
                break
            else:
                print('Неизвестный пункт меню')
        except ValueError:
            print('Неизвестный пункт меню')


if __name__ == '__main__':
    main()
