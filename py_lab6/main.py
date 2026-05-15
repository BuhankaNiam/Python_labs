from fastapi import FastAPI, HTTPException #фреймворк и если будут ошибки
from datetime import datetime #время когда выполнили и когда завершили задачу
from typing import Optional #поле может быть пустым

from models import Task, TaskUpdate #модели
import storage

app = FastAPI()


# ROOT(создание сервера)
@app.get("/") #проверка сервера если кто-то зашёл на "/"
def root():
    return { #ответ пользователю
        "message": "Advanced Task API",
        "version": "2.0"
    }


# CREATE
@app.post("/tasks")
def create_task(task: Task): #FastAPI автоматически проверяет входящие данные
    #провелка уникальности
    if storage.title_exists(task.title):
        raise HTTPException(status_code=400, detail="Title already exists")

    new_task = task.dict() #превращаем объект в словарь
    #добавляем системные поля
    new_task["id"] = storage.get_next_id()
    new_task["created_at"] = datetime.now()
    new_task["completed_at"] = None

    storage.tasks.append(new_task)#сохраняем
    storage.archive_if_needed() #если задач > 20 → старые удаляются в архив

    return new_task


#  GET ALL
@app.get("/tasks")
def get_tasks(
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    limit: Optional[int] = None,
    sort_by: Optional[str] = None
):

    result = storage.tasks.copy() #берём все задачи

    if completed is not None:
        result = [t for t in result if t["completed"] == completed] #берём только выполненое или не выполненое

    if priority:
        result = [t for t in result if t["priority"] == priority]

    if sort_by == "created_at":
        result.sort(key=lambda x: x["created_at"]) #сорт по времени

    if sort_by == "priority":
        result.sort(key=lambda x: storage.priority_value(x["priority"]))  #high → medium → low

    if limit:
        result = result[:limit]

    return result


#  GET ONE
@app.get("/tasks/{task_id}")
def get_task(task_id: int):

    task = storage.find_task(task_id) #ищем задачу по id

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


#  PUT
# заменяешь ВСЕ поля задачи
@app.put("/tasks/{task_id}")
def replace_task(task_id: int, task: Task):

    old = storage.find_task(task_id)

    if not old:
        raise HTTPException(status_code=404, detail="Task not found")

    old.update(task.dict())

    return old


#  PATCH
@app.patch("/tasks/{task_id}") #измени задачу с таким id
def update_task(task_id: int, data: TaskUpdate):

    task = storage.find_task(task_id) #ищем задачу

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in data.dict(exclude_unset=True).items(): #бери только то, что передали
        task[key] = value

    return task


#  COMPLETE
@app.patch("/tasks/{task_id}/complete")
def complete_task(task_id: int):

    task = storage.find_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task["completed"]: #если уже выполнена → нельзя повторно
        raise HTTPException(status_code=400, detail="Already completed")

    task["completed"] = True
    task["completed_at"] = datetime.now()

    return task


#  DELETE
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):

    task = storage.find_task(task_id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    storage.tasks.remove(task)

    return {"message": "Task deleted"}


#  SEARCH
@app.get("/tasks/search") #фильтрует задачи по условиям
def search_tasks(
    keyword: Optional[str] = None,
    priority: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None
):

    result = storage.tasks.copy()

    if keyword: #ищет слово в названии или описании
        result = [
            t for t in result
            if keyword.lower() in t["title"].lower()
            or (t["description"] and keyword.lower() in t["description"].lower())
        ]

    if priority:
        result = [t for t in result if t["priority"] == priority]

    if date_from:
        result = [t for t in result if t["created_at"] >= date_from]

    if date_to:
        result = [t for t in result if t["created_at"] <= date_to]

    return result


#  STATS подсчёты
@app.get("/tasks/stats")
def stats():

    total = len(storage.tasks)#всего задач
    completed = len([t for t in storage.tasks if t["completed"]]) #выполненые
    pending = total - completed #не выполненые

    now = datetime.now()

    overdue = len([ #просроченные
        t for t in storage.tasks
        if t["deadline"]
        and t["deadline"] < now
        and not t["completed"]
    ])

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "overdue": overdue,
        "priority": {
            "high": len([t for t in storage.tasks if t["priority"] == "high"]),
            "medium": len([t for t in storage.tasks if t["priority"] == "medium"]),
            "low": len([t for t in storage.tasks if t["priority"] == "low"])
        }
    }