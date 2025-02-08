import os
import json
import csv
import xml.etree.ElementTree as et
import time
from datetime import datetime, timedelta
import uuid
import random
from typing import Any

OUTPUT_DIR = "/app/output"
INTERVAL = 300

TABLES = ["student", "teacher"]
FORMATS = ["xml", "json", "csv"]


def generate_student() -> dict[str, Any]:
    s = timedelta(seconds=random.randint(1, 120))

    return {
        "id": str(uuid.uuid4()),
        "first_name": random.choice(["Alice", "Bob", "Charlie"]),
        "last_name": random.choice(["Smith", "Jones", "Taylor"]),
        "created_at": (datetime.now() - s).strftime("%Y-%m-%d %H:%M:%S.%f"),
        "deleted_at": None,
    }


def generate_teacher() -> dict[str, Any]:
    first_name = random.choice(["John", "Jane"])
    last_name = random.choice(["Doe", "Brown"])
    s = timedelta(seconds=random.randint(1, 120))

    return {
        "id": str(uuid.uuid4()),
        "first_name": first_name,
        "middle_name": random.choice(["Michael", "Anne"]),
        "last_name": last_name,
        "email": f"{first_name}_{last_name}@bmstu.ru",
        "created_at": (datetime.now() - s).strftime("%Y-%m-%d %H:%M:%S.%f"),
        "deleted_at": None,
    }


GENERATORS = {
    "student": generate_student,
    "teacher": generate_teacher,
}


def save_as_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def save_as_csv(data, file_path):
    keys = data[0].keys()
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)


def save_as_xml(data, file_path):
    root = et.Element("records")
    for record in data:
        record_elem = et.SubElement(root, "record")
        for key, value in record.items():
            elem = et.SubElement(record_elem, key)
            elem.text = str(value) if value is not None else ""

    tree = et.ElementTree(root)
    tree.write(file_path, encoding="utf-8", xml_declaration=True)


def save_data(data, file_path, file_format):
    if file_format == "json":
        save_as_json(data, file_path)
    elif file_format == "csv":
        save_as_csv(data, file_path)
    elif file_format == "xml":
        save_as_xml(data, file_path)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    while True:
        for table_name in TABLES:
            file_id = str(uuid.uuid4())
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_format = random.choice(FORMATS)
            file_name = f"{file_id}_{table_name}_{timestamp}.{file_format}"
            file_path = os.path.join(OUTPUT_DIR, file_name)

            data = [GENERATORS[table_name]() for _ in range(random.randint(100, 1000))]

            save_data(data, file_path, file_format)

            print(f"Файл создан: {file_path}", flush=True)

        time.sleep(INTERVAL)


if __name__ == "__main__":
    main()
