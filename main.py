import re
import random
import time

users = {}
cards = {}

PWD_RE = re.compile(r'^[A-Za-z0-9]{5,}$')

def validate_password(pwd: str) -> bool:
    return bool(PWD_RE.match(pwd))

def register():
    print("\n== Регистрация ==")
    while True:
        username = input("Введите имя пользователя: ").strip()
        if not username:
            print("Имя не может быть пустым.")
            continue
        if username in users:
            print("Имя уже занято, выбери другое.")
            continue
        break

    while True:
        pwd = input("Придумай пароль (только латинские буквы и цифры, минимум 5 символов): ").strip()
        if not validate_password(pwd):
            print("Неправильный формат пароля. Только A-Z, a-z, 0-9 и >=5 символов.")
            continue
        break

    users[username] = pwd
    cards[username] = {}
    print(f"Пользователь {username} успешно зарегистрирован.\n")

def login():
    print("\n== Вход ==")
    username = input("Имя: ").strip()
    pwd = input("Пароль: ").strip()
    if username in users and users[username] == pwd:
        print(f"Добро пожаловать, {username}!\n")
        return username
    else:
        print("Неправильное имя или пароль.\n")
        return None

def add_card(username: str):
    print("\n== Добавление карточки ==")
    while True:
        q = input("Вопрос (или оставь пустым чтобы выйти): ").strip()
        if not q:
            print("Отмена добавления.\n")
            return
        a = input("Ответ: ").strip()
        if not a:
            print("Ответ не может быть пустым. Попробуй снова.")
            continue
        cards[username][q] = a
        print("Карточка добавлена.\n")
        return

def show_random_card(username: str):
    user_cards = cards.get(username, {})
    if not user_cards:
        print("У тебя пока нет карточек.\n")
        return
    q = random.choice(list(user_cards.keys()))
    print("\n== Случайная карточка для повторения ==")
    print("Вопрос:", q)
    see = input("Показать ответ? (y/n): ").strip().lower()
    if see == 'y' or see == 'да' or see == 'd':
        print("Ответ:", user_cards[q])
    print()

def quiz(username: str, per_question_seconds: int = 30):
    user_cards = cards.get(username, {})
    if not user_cards:
        print("У тебя нет карточек — нечего спрашивать.\n")
        return

    qa_list = list(user_cards.items())
    random.shuffle(qa_list)

    correct = 0
    total = 0

    print("\n== Викторина ==")
    print(f"У тебя {len(qa_list)} карточек. На каждый вопрос {per_question_seconds} секунд.")
    print("Вводи 'q' чтобы выйти из викторины раньше.\n")

    for q, a in qa_list:
        total += 1
        print(f"Вопрос {total}: {q}")
        start = time.time()
        ans = input("Ответ: ")
        elapsed = time.time() - start

        if ans.strip().lower() == 'q':
            print("Выход из викторины...\n")
            total -= 1
            break

        if elapsed > per_question_seconds:
            print(f"Время вышло ({elapsed:.1f}s). Переходим к следующему вопросу.\n")
            continue

        if ans.strip().lower() == a.strip().lower():
            print("Верно!\n")
            correct += 1
        else:
            print(f"Неверно. Правильный ответ: {a}\n")

    if total > 0:
        pct = correct / total * 100
        print(f"Викторина окончена. Правильных ответов: {correct}/{total} ({pct:.1f}%).\n")
    else:
        print("Викторина прервана или не проведена.\n")

def user_menu(username: str):
    while True:
        print("=== Меню пользователя ===")
        print("1 - Добавить карточку")
        print("2 - Получить случайную карточку для повторения")
        print("3 - Запустить викторину")
        print("4 - Показать количество карточек")
        print("5 - Выйти (logout)")
        choice = input("Выбери опцию: ").strip()

        if choice == '1':
            add_card(username)
        elif choice == '2':
            show_random_card(username)
        elif choice == '3':
            quiz(username)
        elif choice == '4':
            print(f"У тебя {len(cards.get(username, {}))} карточек.\n")
        elif choice == '5':
            print("Выход из аккаунта.\n")
            return
        else:
            print("Неверная опция.\n")

def main():
    print("Учебная консольная программа — карточки и викторины")
    while True:
        print("=== Главное меню ===")
        print("1 - Регистрация")
        print("2 - Вход")
        print("q - Выход")
        cmd = input("Выбери действие: ").strip().lower()
        if cmd == '1':
            register()
        elif cmd == '2':
            user = login()
            if user:
                user_menu(user)
        elif cmd == 'q':
            print("Пока!")
            break
        else:
            print("Неизвестная команда.\n")

if __name__ == '__main__':
    main()
