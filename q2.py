from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crit_db.db'
db = SQLAlchemy(app)

class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    critic_id = db.Column(db.Integer)

@app.route('/')
def index():
    # Получаем количество уникальных id для каждого critic_id
    critic_counts = db.session.query(Reviews.critic_id, db.func.count(Reviews.id).label('count')).group_by(Reviews.critic_id).all()

    # Создаем таблицу crit_rev_sch в соседней базе данных USERS
    db2 = SQLAlchemy(app, uri='sqlite:///users.db')
    class CritRevSch(db2.Model):
        __tablename__ = 'crit_rev_sch'
        critic_id = db2.Column(db.Integer, primary_key=True)
        count = db2.Column(db.Integer)

    # Удаляем таблицу crit_rev_sch, если она уже существует
    db2.drop_all()

    # Создаем таблицу crit_rev_sch
    db2.create_all()

    # Добавляем данные в таблицу crit_rev_sch
    for critic_id, count in critic_counts:
        crit_rev_sch = CritRevSch(critic_id=critic_id, count=count)
        db2.session.add(crit_rev_sch)

    # Сохраняем изменения в базе данных
    db2.session.commit()

    return 'Done!'

if __name__ == '__main__':
    app.run()


