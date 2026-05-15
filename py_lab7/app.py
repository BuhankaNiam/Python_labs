from flask import Flask, render_template, request, redirect
#Фласк создаёт сайт, рендер показывает html, request берёт данные из формы, redirect перекидывает на другую страницу
import sqlite3
from datetime import datetime
#создаём базу данных
def init_db():
    conn = sqlite3.connect("database.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tracks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            genre TEXT NOT NULL,
            duration INTEGER NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()
app = Flask(__name__) #включаем сервер

DB = "database.db" #подключаем DB

#подключаемя к базе
def get_db():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn

#МАРШРУТЫ
# Главная
@app.route("/")
def index():
    return render_template("index.html")


# Список треков
@app.route("/tracks")
def tracks():
    conn = get_db()
    data = conn.execute("SELECT * FROM tracks").fetchall()
    conn.close()
    return render_template("tracks.html", tracks=data)


# Один трек
@app.route("/tracks/<int:id>")
def track(id):
    conn = get_db()
    data = conn.execute("SELECT * FROM tracks WHERE id=?", (id,)).fetchone() #берём все треки из базы
    conn.close()
    return render_template("track.html", track=data) #отправляем их в html


# Добавление
@app.route("/add", methods=["GET", "POST"]) #GET-открыть форму, POST-отправить данные
def add():
    if request.method == "POST":
        title = request.form["title"]
        artist = request.form["artist"]
        genre = request.form["genre"].lower().capitalize()
        duration = request.form["duration"]

        # валидация
        if not title or not artist or not genre or not duration:
            return "Ошибка: пустые поля"

        try:
            duration = int(duration)
        except:
            return "Ошибка: duration должен быть числом"

        conn = get_db()
        #добавляем в sql
        conn.execute("""
            INSERT INTO tracks (title, artist, genre, duration, created_at) 
            VALUES (?, ?, ?, ?, ?)
        """, (title, artist, genre, duration, datetime.now()))
        conn.commit()
        conn.close()

        return redirect("/tracks")

    return render_template("add.html")


# Статистика
@app.route("/stats")
def stats():
    conn = get_db()

    total = conn.execute("SELECT COUNT(*) FROM tracks").fetchone()[0] #считает сколько всего треков
    avg_duration = conn.execute("SELECT AVG(duration) FROM tracks").fetchone()[0] #считает среднюю продолжительность
    #количество песен по жанрам
    #COUNT(*)-посчитать сколько песен
    by_genre = conn.execute("""
        SELECT genre, COUNT(*) as count 
        FROM tracks
        GROUP BY genre
    """).fetchall()

    conn.close()
    #передаём в html
    return render_template(
        "stats.html",
        total=total,
        avg_duration=avg_duration,
        by_genre=by_genre
    )


if __name__ == "__main__":
    app.run(debug=True)