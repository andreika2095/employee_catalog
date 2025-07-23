# Employee Catalog API

API для управления каталогом сотрудников с иерархической структурой.

## Установка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate    # Windows
Установите зависимости:

bash
pip install -r requirements.txt
Убедитесь, что PostgreSQL запущен и создана БД "ILINE"

Запуск
Генерация тестовых данных (50k сотрудников):

bash
python generate_data.py
Запуск API сервера:

bash
python app.py
Использование
API будет доступно по адресу: http://localhost:8000

Документация Swagger: /docs
Документация ReDoc: /redoc

Конечные точки
GET /employees - список сотрудников (первые 100)
GET /employee/{id} - информация о сотруднике
POST /employee - создание сотрудника
DELETE /employee/{id} - удаление сотрудника