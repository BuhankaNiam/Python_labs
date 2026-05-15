import pandas as pd #работа с таблицами (CSV)
import re #Проверка текста по шаблону
import math
from datetime import datetime
import calendar
from gtts import gTTS #Текст → голос
import tkinter as tk #Интерфейс (окно программы)
from tkinter import messagebox #показывает ошибки


# Обработка даты
def process_birth_date(date_str):
    pattern = r"\d{4}-\d{2}-\d{2}" #проверяем формат

    if not re.match(pattern, date_str):
        raise ValueError("Неверный формат даты!")

    birth_date = datetime.strptime(date_str, "%Y-%m-%d") #превращает текст в настоящую дату и считаем возраст в днях
    today = datetime.now()

    age_days = (today - birth_date).days #возвращает возраст
    weekday = calendar.day_name[birth_date.weekday()] #находит день недели

    return age_days, weekday


# Загрузка CSV
def load_data():
    df = pd.read_csv("orders.csv") #открывает файл как таблицу

    # преобразуем дату
    df["date"] = pd.to_datetime(df["date"], errors='coerce')

    # удаляем пустые строки
    df = df.dropna()

    return df


# Расчёты
def calculate_metrics(df):
    df["total"] = df["price"] * df["quantity"] #cтоимость заказа
    df["final_total"] = df["total"] * (1 - df["discount"]) #цена со скидкой
    df["is_success"] = df["final_total"] > 0 #успешный заказ или нет

    return df


# Анализ
def analyze(df):
        total_income = df["final_total"].sum()#общий доход

        income_by_category = df.groupby("category")["final_total"].sum() #доход по категории
        #групируем по товарам, считаем сколько всего купили, и делаем топ 3
        top_products = df.groupby("product")["quantity"].sum().sort_values(ascending=False).head(3)

        returns_rate = (df["is_success"] == False).mean()#сколько заказов были неуспешными

        return total_income, income_by_category, top_products, returns_rate


# Математика
def math_calculations():
    distance = 100  # км
    speed = 50  # км/ч

    time = distance / speed #время доставки

    # пример с sqrt
    diagonal = math.sqrt(100 ** 2 + 50 ** 2)

    # проверка NaN
    value = float("nan")
    check_nan = math.isnan(value)

    return time, diagonal, check_nan


# Отчёт
def create_report(age_days, weekday, analysis, math_data):
    total_income, income_by_category, top_products, returns_rate = analysis
    time, diagonal, check_nan = math_data
# Создание текста
    report = f""" 
Возраст: {age_days} дней
День рождения: {weekday}

Общий доход: {total_income}

Доход по категориям:
{income_by_category}

Топ товары:
{top_products}

Процент возвратов: {returns_rate}

Время доставки: {time} часов
Диагональ маршрута: {diagonal}
Проверка NaN: {check_nan}
"""

    # сохранить в файл
    with open("report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    return report


# Озвучка
def text_to_speech(text):
    if not text.strip(): #убирает пробелы
        raise ValueError("Текст пуст!") #проверяет не пуст ли текст
    #подключается сервис Google Text-to-Speech
    # Он:берёт текст
    # переводит его в голос
    # использует русский язык (lang='ru')
    tts = gTTS(text=text, lang='ru')
    tts.save("report.mp3")


# Интерфейс
def run_app():
    def process():
        try:
            date = entry.get() #берём дату

            age_days, weekday = process_birth_date(date) #считаем возраст и день ъ
            #загружаем csv и считаем показатели
            df = load_data()
            df = calculate_metrics(df)
            #анилиз
            analysis = analyze(df)
            math_data = math_calculations()
            #отчет
            report = create_report(age_days, weekday, analysis, math_data)
            #Озвучка
            text_to_speech(report)
            #Вывод в окно
            output.delete("1.0", tk.END) #очищает старый текст
            output.insert(tk.END, report) # выводит новый в кно

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))
    #создание окна
    root = tk.Tk()
    root.title("Анализ заказов")
    #текст и кнопки
    tk.Label(root, text="Введите дату рождения (YYYY-MM-DD)").pack()

    entry = tk.Entry(root)
    entry.pack()
    #кнопка запуска
    tk.Button(root, text="Запустить", command=process).pack()

    output = tk.Text(root, height=20, width=60)
    output.pack()

    root.mainloop()


# запуск
run_app()