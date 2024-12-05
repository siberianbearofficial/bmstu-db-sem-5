import json
import csv
import random

# Параметры генерации
MAX_PREREQUISITES_PER_COURSE = 5  # Максимальное количество пререквизитов на один курс
MAX_DEPTH = 3  # Максимальная вложенность пререквизитов


# Функция генерации пререквизитов
def generate_prerequisites(courses):
    course_ids = [course["id"] for course in courses]
    prerequisites = []
    used_pairs = set()  # Чтобы избежать дублирования связей

    def add_prerequisite(course_id, depth):
        if depth > MAX_DEPTH:
            return
        # Случайное количество пререквизитов для текущего курса
        num_prerequisites = random.randint(1, MAX_PREREQUISITES_PER_COURSE)
        selected_ids = random.sample(
            course_ids, min(num_prerequisites, len(course_ids))
        )
        for prereq_id in selected_ids:
            # Избежать петлей и дублирования
            if course_id == prereq_id or (course_id, prereq_id) in used_pairs:
                continue
            prerequisites.append({"course_id": course_id, "prerequisite_id": prereq_id})
            used_pairs.add((course_id, prereq_id))
            # Рекурсивно добавляем зависимости для пререквизита
            if random.random() < 0.5:  # Вероятность углубления
                add_prerequisite(prereq_id, depth + 1)

    # Генерация пререквизитов для каждого курса
    for course in courses:
        add_prerequisite(course["id"], depth=1)

    return prerequisites


# Основной код
def main():
    input_file = "data/course.json"
    output_file = "data/course_prerequisite.csv"

    # Загрузка курсов из файла
    with open(input_file, "r", encoding="utf-8") as f:
        courses = json.load(f)

    # Генерация данных о пререквизитах
    prerequisites = generate_prerequisites(courses)

    # Сохранение результатов в CSV
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["course_id", "prerequisite_id"])
        writer.writeheader()  # Записываем заголовок
        writer.writerows(prerequisites)

    print(f"Генерация завершена. Пререквизиты сохранены в '{output_file}'.")


if __name__ == "__main__":
    main()
