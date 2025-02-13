import psycopg2

from menu import menu
from task import task1, task2, task3, task4, task5, task6, task7, task8, task9, task10


def main():
    try:
        con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432",
        )
    except Exception as e:
        print(f"Ошибка при подключении к БД: {e}")
        return

    menu(
        ("Скалярный запрос", lambda: task1(con)),
        ("Запрос с JOIN", lambda: task2(con)),
        ("Запрос с CTE и оконными функциями", lambda: task3(con)),
        ("Запрос к метаданным", lambda: task4(con)),
        ("Вызов скалярной функции", lambda: task5(con)),
        ("Вызов табличной функции", lambda: task6(con)),
        ("Вызов хранимой процедуры", lambda: task7(con)),
        ("Вызов системной функции", lambda: task8(con)),
        ("Создание таблицы", lambda: task9(con)),
        ("Вставка данных в таблицу", lambda: task10(con)),
    )

    con.close()


if __name__ == "__main__":
    main()
