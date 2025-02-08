# Ultimate Data Generation and ETL with NiFi

## Состав
- `file_generator`: Генерация файлов (рандомные данные и рандомный формат из JSON/XML/CSV)
- `nifi`: Apache NiFi для обработки данных - ETL
- `db`: PostgreSQL с таблицами, в которые NiFi будет раскладывать данные из файлов

## Запуск
1. Убедитесь, что у вас установлен Docker и Docker Compose
2. Запустите проект:
   ```bash
   docker-compose up --build
   ```
3. NiFi доступен по адресу http://localhost:8080.
4. PostgreSQL доступен на localhost:5432 (логин/пароль: admin/admin).

## Настройка NiFi
Настройте процессоры:
- GetFile: Читает из /input_files
- ConvertRecord: Конвертирует файлы
- SplitJSON, ConvertJSONToSQL, PutSQL
- Настройте соединение с PostgreSQL
