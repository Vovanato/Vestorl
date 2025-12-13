☁️ Vestorl Cloud File Manager

Веб-додаток для безпечного зберігання та управління файлами у хмарному сховищі Azure Blob Storage.
Проєкт реалізовано як курсову роботу з використанням сучасного стеку технологій: Python, Flask, Docker та хмарних сервісів.

🚀 Функціонал

Автентифікація: Реєстрація та вхід користувачів (з хешуванням паролів).

Завантаження файлів: Користувачі можуть завантажувати файли будь-якого формату.

Хмарне зберігання: Файли фізично зберігаються в Microsoft Azure, що гарантує надійність.

Управління: Перегляд списку власних файлів та їх видалення.

Безпека:

Використання сесій для захисту доступу.

Валідація вхідних даних.

Унікальні імена файлів (UUID) для уникнення конфліктів.

🛠️ Технології

Backend

Python 3.12

Flask — веб-фреймворк.

MySQL Connector — драйвер бази даних.

Azure Storage Blob — SDK для роботи з хмарою.

Frontend

HTML5 / CSS3 — адаптивний дизайн.

JavaScript (Fetch API) — асинхронна взаємодія з сервером (AJAX).

Інфраструктура

MySQL — реляційна база даних для зберігання метаданих.

Microsoft Azure — Blob Storage контейнер.

Docker — контейнеризація для легкого розгортання.

⚙️ Налаштування перед запуском

Перед запуском необхідно створити файл .env у корені проєкту. Використовуйте файл env.template як зразок.

SECRET_KEY=ваш_секретний_ключ_flask
AZURE_CONNECTION_STRING=ваш_рядок_підключення_azure
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=ващ_пароль_mysql
DB_NAME=CLOUD


Налаштування Бази Даних (SQL)

Виконайте цей SQL-скрипт у вашій MySQL базі даних перед запуском:

CREATE DATABASE IF NOT EXISTS CLOUD;
USE CLOUD;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE files (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    filename VARCHAR(255) NOT NULL,
    storage_name VARCHAR(255) NOT NULL,
    file_url TEXT NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);


🏃‍♂️ Як запустити (Локально)

Клонуйте репозиторій:

git clone [https://github.com/ВАШ_НІК/Vestorl.git](https://github.com/ВАШ_НІК/Vestorl.git)
cd Vestorl


Створіть віртуальне середовище:

python3 -m venv .venv
source .venv/bin/activate  # Для Linux/MacOS
# .\.venv\Scripts\Activate # Для Windows


Встановіть залежності:

pip install -r requirements.txt


Запустіть сервер:

python run.py


Відкрийте браузер за адресою: http://127.0.0.1:5000

🐳 Як запустити (через Docker)

Це найпростіший спосіб запуску, який гарантує роботу на будь-якій машині.

Збірка образу:

docker build -t vestorl-app .


Запуск контейнера:
Примітка: ми використовуємо --network="host", щоб контейнер мав доступ до локальної MySQL.

docker run --network="host" --env-file .env vestorl-app


Додаток буде доступний за адресою: http://localhost:5000

📂 Структура проєкту

Vestorl/
├── app/
│   ├── routes/          # Логіка (API та Сторінки)
│   ├── static/          # CSS стилі
│   ├── templates/       # HTML шаблони
│   ├── database.py      # Підключення до MySQL
│   └── storage.py       # Робота з Azure Blob
├── .env                 # Секретні ключі (не пушити в Git!)
├── .gitignore           # Правила ігнорування
├── Dockerfile           # Інструкція для Docker
├── requirements.txt     # Список бібліотек
└── run.py               # Точка входу в додаток


