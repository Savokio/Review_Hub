from flask import Flask
import mysql.connector
from flask import current_app,g
import json

app = Flask(__name__)

"g делает переменую глобальной во всём фласк приложении"

@app.route('/critics', methods=['GET'])
def get_crit_db(): #функция возращает даные из таблицы критик - имя,кол-во обзоров,средную оценку
    if 'db' not in g or not g.db.is_connected():
        g.crit_db = mysql.connector.connect(
            host='localhost',
            user='Savokio',
            password='Stigmata',
            database='crit_db'
        )
    return g.crit_db


def close_crit_db(e=None):
    crit_db = g.pop('db', None)

    if crit_db is not None and crit_db.is_connected():
        crit_db.close()

def init_app(app):
    app.teardown_appcontext(close_crit_db)

def get_crit_info():
    db = get_crit_db()
    cursor = db.cursor(buffered=True) #буфер для работы fetchone присутствует
    cursor.execute("SELECT * FROM crit_db.Critics")
    json_data = [] #заготовка для файла json
    row_headers=["id","name","review_amount","avg_review"] #даёт наименования
    Critic_info = cursor.fetchall()
    for res in Critic_info:
        json_data.append(dict(zip(row_headers,res)))
    cursor.close()
    dump=json.dumps(json_data)
    loaded_r = json.loads(dump)
    return loaded_r

"""Даёт данные о обзорах определенного критика order - то как сортировать список """
def get_crit_reviews(id,order=""): 
    db = get_crit_db()
    cursor = db.cursor(buffered=True) 
    cursor.execute("""SELECT  reviews.Critic_score, films.Film_name,reviews.Summary_text,reviews.Link
    FROM reviews
    INNER JOIN Films
    on reviews.FIlm_id=films.id
    INNER JOIN Critics
    on reviews.Critic_id=critics.id
    where critics.id="""+str(id)+"\n    "+order)  
    json_data = [] #заготовка для файла json
    row_headers=["crit_score","Film_name","review_summary"] #даёт наименования
    Critic_info = cursor.fetchall()
    for res in Critic_info:
        json_data.append(dict(zip(row_headers,res)))
    cursor.close()
    dump=json.dumps(json_data)
    loaded_r = json.loads(dump)
    return loaded_r
