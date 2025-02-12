from typing import Optional

import psycopg2
import redis
import time
import threading
import argparse
import uuid
import random
import datetime
import matplotlib.pyplot as plt

running = True


def query_loop(db_conn, redis_client, query, interval, timings_list):
    while running:
        db_start = time.time()
        cur = db_conn.cursor()
        cur.execute(query)
        result_db = cur.fetchall()
        cur.close()
        db_elapsed = time.time() - db_start

        redis_key = "stats"
        redis_start = time.time()
        cached_result = redis_client.get(redis_key)
        if cached_result is None:
            cur = db_conn.cursor()
            cur.execute(query)
            result_for_cache = cur.fetchall()
            cur.close()

            redis_client.set(redis_key, str(result_for_cache))

        redis_elapsed = time.time() - redis_start

        timestamp = datetime.datetime.now()
        timings_list.append((timestamp, db_elapsed, redis_elapsed))
        print(
            f"{timestamp} - DB query time: {db_elapsed:.4f}s, Redis query time: {redis_elapsed:.4f}s"
        )
        time.sleep(interval)


def modification_loop(db_conn, mode, interval, inserted_ids):
    while running:
        time.sleep(interval)
        if mode == "insert":
            cur = db_conn.cursor()
            cur.execute("SELECT id FROM teacher LIMIT 1;")
            teacher = cur.fetchone()
            if teacher is None:
                print("Нет учителей в базе, невозможно вставить курс.")
            else:
                teacher_id = teacher[0]
                new_id = str(uuid.uuid4())
                title = f"Новый курс {new_id[:8]}"
                description = "Описание нового курса"
                now = datetime.datetime.now()
                cur.execute(
                    "INSERT INTO course (id, title, description, teacher_id, created_at) VALUES (%s, %s, %s, %s, %s);",
                    (new_id, title, description, teacher_id, now),
                )
                db_conn.commit()
                inserted_ids.append(new_id)
                print(f"Вставлен новый курс: {title}")
            cur.close()

        elif mode == "delete":
            if inserted_ids:
                course_id = inserted_ids.pop(0)
                cur = db_conn.cursor()
                cur.execute("DELETE FROM course WHERE id = %s;", (course_id,))
                db_conn.commit()
                print(f"Удален курс с id: {course_id}")
                cur.close()
            else:
                print("Нет курсов для удаления.")

        elif mode == "update":
            cur = db_conn.cursor()
            cur.execute("SELECT id, title FROM course LIMIT 10;")
            courses = cur.fetchall()
            if courses:
                course = random.choice(courses)
                new_title = course[1] + " (new)"
                cur.execute(
                    "UPDATE course SET title = %s WHERE id = %s;",
                    (new_title, course[0]),
                )
                db_conn.commit()
                print(f"Обновлен курс с id: {course[0]}, новое название: {new_title}")
            else:
                print("Нет курсов для обновления.")
            cur.close()


def main():
    parser = argparse.ArgumentParser(
        description="Сравнительный анализ времени выполнения запросов через БД и Redis с модификациями"
    )
    parser.add_argument(
        "--mode",
        type=str,
        choices=["none", "insert", "delete", "update"],
        default="none",
        help="Режим модификации: none, insert, delete, update",
    )
    parser.add_argument(
        "--runtime", type=int, default=60, help="Общее время выполнения (в секундах)"
    )
    args = parser.parse_args()

    db_conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="postgres",
    )

    redis_client = redis.Redis(host="localhost", port=6379)

    query = """
    SELECT c.title, COUNT(e.id) AS enrollment_count
    FROM course c
    LEFT JOIN enrollment e ON c.id = e.course_id
    WHERE c.deleted_at IS NULL
    GROUP BY c.id, c.title
    ORDER BY enrollment_count DESC
    LIMIT 10;
    """

    timings = []  # Каждый элемент: (timestamp, db_time, redis_time)
    inserted_ids = []  # Для delete

    query_thread = threading.Thread(
        target=query_loop, args=(db_conn, redis_client, query, 5, timings)
    )
    query_thread.start()

    mod_thread: Optional[threading.Thread] = None
    if args.mode != "none":
        mod_thread = threading.Thread(
            target=modification_loop, args=(db_conn, args.mode, 10, inserted_ids)
        )
        mod_thread.start()

    start_time = time.time()
    while time.time() - start_time < args.runtime:
        time.sleep(1)
    global running
    running = False

    query_thread.join()
    if mod_thread:
        mod_thread.join()

    db_conn.close()

    timestamps, db_times, redis_times = zip(*timings)

    plt.figure(figsize=(10, 5))
    plt.plot(timestamps, db_times, marker="o", label="DB Query Time")
    plt.plot(timestamps, redis_times, marker="x", label="Redis Query Time")
    plt.xlabel("Время")
    plt.ylabel("Время выполнения (сек)")
    plt.title(f"Сравнение времени выполнения запросов ({args.mode} режим)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{args.mode}.png")


if __name__ == "__main__":
    main()
