import psycopg2


# 10 курсов с наибольшим количеством записей
QUERY = """
SELECT c.title, COUNT(e.id) AS enrollment_count
FROM course c
LEFT JOIN enrollment e ON c.id = e.course_id
WHERE c.deleted_at IS NULL
GROUP BY c.id, c.title
ORDER BY enrollment_count DESC
LIMIT 10;
"""


def main():
    with psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(QUERY)
            rows = cur.fetchall()

    print("Топ 10 курсов по количеству зачисленных студентов:")
    for row in rows:
        print(f"Курс: {row[0]}, Количество зачислений: {row[1]}")


if __name__ == "__main__":
    main()
