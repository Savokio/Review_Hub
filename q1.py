from flask import Flask, jsonify
import MySQLdb

app = Flask(__name__)

@app.route('/critic_reviews', methods=['GET'])
def get_critic_reviews():
    # Подключение к базе данных crit_db
    crit_db = MySQLdb.connect(
        host='localhost',
        user='Savokio',
        password='Stigmata',
        db='crit_db'
    )
    cursor = crit_db.cursor()

    # Выполнение запроса для получения количества уникальных обзоров для каждого критика
    cursor.execute("""
        SELECT Critic_id, COUNT(DISTINCT id) AS review_count
        FROM Reviews
        GROUP BY Critic_id
    """)
    results = cursor.fetchall()

    # Закрываем курсор и соединение с базой данных
    cursor.close()
    crit_db.close()

    # Формирование словаря с данными
    critic_reviews = {}
    for row in results:
        critic_reviews[row[0]] = row[1]

    return jsonify(critic_reviews)

@app.route('/create_table', methods=['GET'])
def create_table():
    # Подключение к базе данных USERS
    users_db = MySQLdb.connect(
        host='localhost',
        user='Service_11',
        password='qwerty',
        db='USERS'
    )
    cursor = users_db.cursor()

    # Удаление таблицы crit_rev_sch, если она существует
    cursor.execute("""
        DROP TABLE IF EXISTS crit_rev_sch
    """)

    # Создание таблицы crit_rev_sch
    cursor.execute("""
        CREATE TABLE crit_rev_sch (
            Critic_id INT NOT NULL,
            Review_count INT NOT NULL
        )
    """)

    # Фиксация изменений и закрытие курсора и соединения с базой данных
    users_db.commit()
    cursor.close()
    users_db.close()

    return jsonify({ 'message': 'Таблица crit_rev_sch создана' })

if __name__ == '__main__':
    app.run()
