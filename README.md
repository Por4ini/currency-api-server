Для розгортання проекту необхідно виконати наступні кроки:

Клонуйте репозиторій на свій комп'ютер за допомогою команди: 

git clone https://github.com/Por4ini/currency-api-server.git

Перейдіть в директорію з проектом:

cd currency-api-server

Створіть віртуальне оточення 

python3 -m venv venv

source venv/bin/activate

Встановіть залежності за допомогою менеджера пакетів pip:

pip install -r requirements.txt

Додайте данні для підключення до вашої бд(Postgresql): 

app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://<USERNAME>:<PASSWORD>@<HOST>:<PORT>/<DATABASE>"

Запустіть міграції для створення бази даних:
    
flask db migrate
    
flask db upgrade

Запустіть сервер за допомогою команди:
    
flask run

Запустіть тести test.py

API документація у swagger: http://127.0.0.1:5000/swagger/

Отримати актуальний курс будь-якої валюти до долара США: 
    
    http://127.0.0.1:5000/api/UAH 
    
Для валют зі списку (UAH, PLN, EUR, CAD) – автоматично зберегається отриманий курс до бази даних.

Отримати всі записи з бази данних: http://127.0.0.1:5000/api/all

Отримати історію курсів з бази даних з можливістю відфільтрувати за періодом та валютою: 
    
http://127.0.0.1:5000/api/UAH&2023-02-20

Використання директиви cron для отримання нових курсів із певною періодичністю:
Відкрити файл в консолі: EDITOR=nano crontab -e
Вставити значення: 
0 1 * * * curl --request POST 'http://localhost:5000/api/add' --header 'Content-Type: application/json' --data '{"currency_code":"CAD"}' && \
    curl --request POST 'http://localhost:5000/api/add' --header 'Content-Type: application/json' --data '{"currency_code":"UAH"}' && \
    curl --request POST 'http://localhost:5000/api/add' --header 'Content-Type: application/json' --data '{"currency_code":"EUR"}' && \
    curl --request POST 'http://localhost:5000/api/add' --header 'Content-Type: application/json' --data '{"currency_code":"PLN"}'
Зберегти файл зі списком задач і вийти з редактора.

