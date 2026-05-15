from functions import *

teachers = load_data()

while True:

    print("\nMENU")
    print("1 Добавить преподавателя")
    print("2 Добавить дисциплину")
    print("3 Показать преподавателей")
    print("4 Удалить преподавателя")
    print("5 Найти преподавателя")
    print("6 Уникальные дисциплины")
    print("7 Количество данных")
    print("8 Преподаватель с максимум дисциплин")
    print("9 Сохранить")
    print("10 Выход")

    choice = input("Выберите пункт: ")

    if choice == "1":
        add_teacher(teachers)

    elif choice == "2":
        add_subject(teachers)

    elif choice == "3":
        show_teachers(teachers)

    elif choice == "4":
        delete_teacher(teachers)

    elif choice == "5":
        search_teacher(teachers)

    elif choice == "6":
        unique_subjects(teachers)

    elif choice == "7":
        count_data(teachers)

    elif choice == "8":
        teacher_with_most_subjects(teachers)

    elif choice == "9":
        save_data(teachers)
        print("Сохранено")

    elif choice == "10":
        save_data(teachers)
        break

    else:
        print("Неверный выбор")