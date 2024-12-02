from flask import Flask, jsonify, request, send_file, send_from_directory,render_template
import mysql.connector
app = Flask(__name__)
from crit_info import get_crit_db, close_crit_db, get_crit_info
import json


@app.route('/templates/<path:filename>')
def serve_templates_file(filename):
    return send_from_directory("", filename)

# @app.route('/static/<path:filename>')
# def serve_static_file(filename):
#     return send_from_directory("", filename)

@app.route('/css/<path:filename>')
def serve_css_file(filename):
    return send_from_directory("./static/css", filename)

@app.route('/img/<path:filename>')
def serve_img_file(filename):
    return send_from_directory("./static/img", filename)



"""Чтобы jinja,которая мне нужна для вставления данных из нашей базы работала (плюс лупы,которые могут дублировать обьекты в html файле),
каждая страница должна пройти через фунуцию "render_template",так что извинаюсь за перелопачивание вашего кода """

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template("index.html", info=get_crit_info())



@app.route('/about', methods = ['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/profile', methods = ['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    return  render_template('log.html')




@app.route('/register', methods = ['GET', 'POST'])
def register():
    return render_template('reg.html')

@app.route('/critics', methods = ['GET', 'POST']) #все критики
def crit_library():
    return render_template('crit_lib.html',info=get_crit_info())


@app.route('/submit_login', methods=['POST'])
def get_login_request():
    # Получаем данные из запроса
    login = request.form.get('login')
    password = request.form.get('password')
    # Обрабатываем данные

    #file_path = 'login-result.html'


    #processed_data = process_data(file_path)
    processed_data = f'Вот что мы получили {login} {password}'
    # Возвращаем результат
    return processed_data


# def process_data(file_path):
#     # Получаем данные из запроса
#     # Проверяем, что файл существует
#     if file_path:
#         # Возвращаем содержимое файла
#         return render_template(file_path, as_attachment=False)
#     return "Файл не найден", 404



if __name__ == '__main__':
    app.run(debug=True, host = '0.0.0.0')
