INSERT INTO student_profile (id, student_id, profile_data, created_at) VALUES
('11111111-1111-1111-1111-111111111111', 'ae3f8fae-ee2a-4de0-83e8-0bd146506be3',
 '{
   "full_name": "Иванов Иван Иванович",
   "email": "ivanov@example.com",
   "phone": "+7 999 123-45-67",
   "address": {
     "city": "Москва",
     "street": "Ленина",
     "house": "15",
     "apartment": "42"
   },
   "hobbies": ["футбол", "программирование", "чтение"],
   "achievements": [
     {"title": "Победитель олимпиады по математике", "year": 2022},
     {"title": "Участник хакатона", "year": 2023}
   ]
 }', NOW()),

('33333333-3333-3333-3333-333333333333', '45a063db-8ac8-4eb4-8a7b-7cff542525d5',
 '{
   "full_name": "Петрова Анна Сергеевна",
   "email": "petrova@example.com",
   "phone": "+7 999 765-43-21",
   "address": {
     "city": "Санкт-Петербург",
     "street": "Пушкина",
     "house": "10",
     "apartment": "7"
   },
   "hobbies": ["рисование", "музыка", "путешествия"],
   "achievements": [
     {"title": "Лучший проект на курсе", "year": 2021},
     {"title": "Сертификат по английскому языку", "year": 2022}
   ]
 }', NOW()),

('55555555-5555-5555-5555-555555555555', '97d3fabe-677f-4a82-bafe-62e6944a241c',
 '{
   "full_name": "Сидоров Алексей Владимирович",
   "email": "sidorov@example.com",
   "phone": "+7 999 555-55-55",
   "address": {
     "city": "Новосибирск",
     "street": "Мира",
     "house": "25",
     "apartment": "13"
   },
   "hobbies": ["шахматы", "настольные игры", "кино"],
   "achievements": [
     {"title": "Победитель турнира по шахматам", "year": 2020},
     {"title": "Участник конференции по ИИ", "year": 2023}
   ]
 }', NOW()),

('77777777-7777-7777-7777-777777777777', 'ac63aba6-f605-4d4c-a36e-627a9d84b27c',
 '{
   "full_name": "Козлова Екатерина Дмитриевна",
   "email": "kozlova@example.com",
   "phone": "+7 999 888-77-66",
   "address": {
     "city": "Екатеринбург",
     "street": "Свердлова",
     "house": "5",
     "apartment": "9"
   },
   "hobbies": ["танцы", "йога", "фотография"],
   "achievements": [
     {"title": "Победитель конкурса танцев", "year": 2021},
     {"title": "Организатор фотовыставки", "year": 2022}
   ]
 }', NOW()),

('99999999-9999-9999-9999-999999999999', 'c3cb90e1-590c-4be1-a4a5-48f2c72a4123',
 '{
   "full_name": "Морозов Денис Андреевич",
   "email": "morozov@example.com",
   "phone": "+7 999 111-22-33",
   "address": {
     "city": "Казань",
     "street": "Толстого",
     "house": "3",
     "apartment": "12"
   },
   "hobbies": ["плавание", "велоспорт", "программирование"],
   "achievements": [
     {"title": "Сертификат по Python", "year": 2022},
     {"title": "Участник марафона", "year": 2023}
   ]
 }', NOW());
