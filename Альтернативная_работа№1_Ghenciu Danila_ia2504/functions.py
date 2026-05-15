import re

FILE_NAME = "teachers.txt"

def load_data():
    teachers = {}
    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                name, subjects = line.strip().split(":")
                teachers[name] = subjects.split(",")
    except:
        pass
    return teachers

def save_data(teachers):
    with open(FILE_NAME, "w") as file:
        for teacher, subjects in teachers.items():
            line = teacher + ":" + ",".join(subjects)
            file.write(line + "\n")

def validate_name(name):
    pattern = r'^[A-Za-z-]{1,30}_[A-Za-z-]{1,30}$'
    return re.match(pattern, name)

def validate_subject(subject):
    pattern = r'^[A-Za-z0-9 ]{2,50}$'
    return re.match(pattern, subject)

def add_teacher(teachers):
    name = input("Введите имя и фамилию (Name_Surname): ")

    if not validate_name(name):
        print("Неверный формат имени")
        return

    if name in teachers:
        print("Такой преподаватель уже существует")
        return

    teachers[name] = []
    print("Преподаватель добавлен")

def add_subject(teachers):
    name = input("Введите преподавателя: ")

    if name not in teachers:
        print("Преподаватель не найден")
        return

    while True:
        subject = input("Введите дисциплину: ")

        if not validate_subject(subject):
            print("Неверное название")
            continue

        if subject in teachers[name]:
            print("Дисциплина уже существует")
        else:
            teachers[name].append(subject)
            print("Дисциплина добавлена")

        answer = input("Добавить еще? (Y/N): ").lower()
        if answer != "y":
            break

def show_teachers(teachers):
    for teacher, subjects in teachers.items():
        print(teacher, "->", subjects)
        print("Количество дисциплин:", len(subjects))

def delete_teacher(teachers):
    name = input("Введите преподавателя для удаления: ")

    if name in teachers:
        confirm = input("Удалить? (Y/N): ").lower()
        if confirm == "y":
            del teachers[name]
            print("Удалено")
    else:
        print("Не найден")

def search_teacher(teachers):
    name = input("Введите имя преподавателя: ")

    if name in teachers:
        print("Дисциплины:", teachers[name])
    else:
        print("Не найден")

def unique_subjects(teachers):
    subjects = set()
    for sublist in teachers.values():
        for s in sublist:
            subjects.add(s)

    for s in sorted(subjects):
        print(s)

def count_data(teachers):
    total_teachers = len(teachers)
    total_subjects = sum(len(sublist) for sublist in teachers.values())
    print("Преподавателей:", total_teachers)
    print("Дисциплин:", total_subjects)

def teacher_with_most_subjects(teachers):
    max_count = 0
    for subjects in teachers.values():
        if len(subjects) > max_count:
            max_count = len(subjects)

    for teacher, subjects in teachers.items():
        if len(subjects) == max_count:
            print("Больше всего дисциплин у:", teacher)