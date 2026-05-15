from datetime import datetime

tasks = [] #база данных
archived_tasks = []

current_id = 1 #счётчик


def get_next_id():
    global current_id
    _id = current_id
    current_id += 1
    return _id


def find_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None

#проверяет создал ли уже задача
def title_exists(title: str):
    for t in tasks:
        if t["title"].lower() == title.lower():
            return True
    return False

#сортировка по значимости
def priority_value(priority: str):
    return {
        "high": 1,
        "medium": 2,
        "low": 3
    }.get(priority, 99)

#помещаем в архив если больше 20
def archive_if_needed():
    while len(tasks) > 20:
        archived_tasks.append(tasks.pop(0))