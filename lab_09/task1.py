import psycopg2


def main():
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    )
    cur = conn.cursor()

    # 10 курсов с наибольшим количеством записей
    query = """
    SELECT c.title, COUNT(e.id) AS enrollment_count
    FROM course c
    LEFT JOIN enrollment e ON c.id = e.course_id
    WHERE c.deleted_at IS NULL
    GROUP BY c.id, c.title
    ORDER BY enrollment_count DESC
    LIMIT 10;
    """

    cur.execute(query)
    rows = cur.fetchall()

    print("Топ 10 курсов по количеству зачисленных студентов:")
    for row in rows:
        print(f"Курс: {row[0]}, Количество зачислений: {row[1]}")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()
