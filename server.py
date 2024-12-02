
import mysql.connector

def insert_data_to_users_table(data):
    # Подключение к базе данных
    cnx = mysql.connector.connect(user='Service_11', password='qwerty',
                                  host='localhost',
                                  database='USERS')

    # Создание курсора
    cursor = cnx.cursor()

    # SQL-запрос для вставки данных
    query = ("INSERT INTO Users (First_Name, Last_Name, Age, Role, Email_Address, Biography)"
             "VALUES (%s, %s, %s, %s, %s, %s);")

    #query = ("INSERT INTO Users (column1, column2, column3) "
     #        "VALUES (%s, %s, %s)")

    # Данные для вставки
    cursor.execute(query, data)

    # Фиксация изменений
    cnx.commit()

    # Закрытие курсора и соединения
    cursor.close()
    cnx.close()


if __name__ == '__main__':
    # app.run(debug=True)
    insert_data_to_users_table(('Tomas', 'Doe', 30, 'Reader', 'john.doe@example.com', 'This is a biography of John Doe'))
