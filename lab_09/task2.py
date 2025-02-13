import redis.asyncio as redis
import time
import uuid
import random
import asyncio
import asyncpg
import matplotlib.pyplot as plt

from datetime import datetime


COUNT = 20
MEASURE_COUNT = 5
QUERY_LOOP_DELAY = 0.5  # 5 sec
MODIFICATION_LOOP_DELAY = 1  # 10 sec
REDIS_KEY = "stats"

QUERY = """
SELECT c.title, COUNT(e.id) AS enrollment_count
FROM course c
LEFT JOIN enrollment e ON c.id = e.course_id
WHERE c.deleted_at IS NULL
GROUP BY c.id, c.title
ORDER BY enrollment_count DESC
LIMIT 10;
"""


async def create_db_conn() -> asyncpg.Connection:
    return await asyncpg.connect(
        host="localhost",
        port=5432,
        database="postgres",
        user="postgres",
        password="postgres",
    )


async def measure_db(db_conn: asyncpg.Connection):
    start = time.time()
    await db_conn.execute(QUERY)
    return time.time() - start


async def measure_redis(db_conn: asyncpg.Connection, redis_client: redis.Redis):
    start = time.time()
    cached_result = await redis_client.get(REDIS_KEY)
    if cached_result is None:
        result_for_cache = await db_conn.fetch(QUERY)
        await redis_client.set(REDIS_KEY, str(result_for_cache))
    return time.time() - start


async def invalidate_cache(redis_client: redis.Redis):
    await redis_client.delete(REDIS_KEY)


async def query_loop(
    db_conn: asyncpg.Connection,
    redis_client: redis.Redis,
    timings: list[dict[str, float]],
) -> None:
    for i in range(COUNT):
        postgres_time = await measure_db(db_conn)
        redis_time = await measure_redis(db_conn, redis_client)
        timings.append(
            {
                "postgres": postgres_time,
                "redis": redis_time,
            }
        )
        print(f"[#{i + 1}] postgres: {postgres_time:.4f}s, redis: {redis_time:.4f}s")
        await asyncio.sleep(QUERY_LOOP_DELAY)


async def modification_loop(
    db_conn: asyncpg.Connection,
    redis_client: redis.Redis,
    mode: str,
    inserted_ids: list[str],
) -> None:
    while True:
        await asyncio.sleep(MODIFICATION_LOOP_DELAY)
        if mode == "insert":
            teacher_id = await db_conn.fetchval("SELECT id FROM teacher LIMIT 1;")
            if teacher_id is None:
                print("Нет учителей в базе, невозможно вставить курс.")
            else:
                new_id = str(uuid.uuid4())
                title = f"Новый курс {new_id[:8]}"
                await db_conn.execute(
                    "INSERT INTO course (id, title, description, teacher_id, created_at) VALUES ($1, $2, $3, $4, $5);",
                    new_id,
                    title,
                    "Описание нового курса",
                    teacher_id,
                    datetime.now(),
                )
                inserted_ids.append(new_id)
                await invalidate_cache(redis_client)
                print(f"Вставлен новый курс: {title}")

        elif mode == "delete":
            if inserted_ids:
                course_id = inserted_ids.pop(0)
                await db_conn.execute("DELETE FROM course WHERE id = $1;", course_id)
                await invalidate_cache(redis_client)
                print(f"Удален курс с id: {course_id}")
            else:
                print("Нет курсов для удаления.")

        elif mode == "update":
            courses = await db_conn.fetch("SELECT id, title FROM course LIMIT 10;")
            if courses:
                course = random.choice(courses)
                new_title = course[1] + " (new)"
                await db_conn.execute(
                    "UPDATE course SET title = $1 WHERE id = $2;",
                    new_title,
                    course[0],
                )
                await invalidate_cache(redis_client)
                print(f"Обновлен курс с id: {course[0]}, новое название: {new_title}")
            else:
                print("Нет курсов для обновления.")


async def measure(
    query_conn: asyncpg.Connection,
    mod_conn: asyncpg.Connection,
    redis_client: redis.Redis,
    mode: str,
    inserted_ids: list[str],
) -> list[dict[str, float]]:
    timings = list()

    mod_loop_task = None
    if mode != "none":
        mod_loop_task = asyncio.create_task(
            modification_loop(query_conn, redis_client, mode, inserted_ids)
        )

    await query_loop(mod_conn, redis_client, timings)
    if mod_loop_task is not None:
        mod_loop_task.cancel()

    return timings


async def measure_average(
    query_conn: asyncpg.Connection,
    mod_conn: asyncpg.Connection,
    redis_client: redis.Redis,
    mode: str,
    inserted_ids: list[str],
) -> list[dict[str, float]]:
    timings = [
        {
            "postgres": 0.0,
            "redis": 0.0,
        }
        for _ in range(COUNT)
    ]

    for j in range(MEASURE_COUNT):
        print(f"-- attempt {j + 1} ---")
        for i, t in enumerate(
            await measure(query_conn, mod_conn, redis_client, mode, inserted_ids)
        ):
            timings[i]["postgres"] += t["postgres"]
            timings[i]["redis"] += t["redis"]

    for i in range(COUNT):
        timings[i]["postgres"] = timings[i]["postgres"] / MEASURE_COUNT
        timings[i]["redis"] = timings[i]["redis"] / MEASURE_COUNT

    return timings


def plot(mode: str, timings: list[dict[str, float]]) -> None:
    attempts = range(1, COUNT + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(
        attempts,
        tuple(map(lambda t: t["postgres"], timings)),
        marker="o",
        label="DB Query Time",
    )
    plt.plot(
        attempts,
        tuple(map(lambda t: t["redis"], timings)),
        marker="x",
        label="Redis Query Time",
    )
    plt.xlabel("Количество попыток")
    plt.ylabel("Время выполнения (сек)")
    plt.title(f"Сравнение времени выполнения запросов ({mode} режим)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{mode}.png")


async def main() -> None:
    redis_client = redis.Redis(host="localhost", port=6379)

    query_conn = await create_db_conn()
    mod_conn = await create_db_conn()

    inserted_ids = list()  # общий пул добавленных записей для delete
    all_timings = dict()
    for mode in ("none", "insert", "update", "delete"):
        print(f"----- measuring timings for mode: {mode} -----")
        all_timings[mode] = await measure_average(
            query_conn, mod_conn, redis_client, mode, inserted_ids
        )

    await query_conn.close()
    await mod_conn.close()

    for mode, timings in all_timings.items():
        plot(mode, timings)


if __name__ == "__main__":
    asyncio.run(main())
