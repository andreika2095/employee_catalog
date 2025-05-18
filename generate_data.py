from faker import Faker
import random
import psycopg2

# Инициализация Faker
fake = Faker('ru_RU')
Faker.seed(4321)

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="ILINE",
    user="postgres",
    password="postgres",
    host="localhost"
)
cur = conn.cursor()

# Первый сотрудник (CEO), у которого нет руководителя
first_employee = ('Иван Петров', 'CEO', '2020-01-01', 150000, None)
cur.execute('''
    INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
    VALUES (%s, %s, %s, %s, %s)
''', first_employee)

# Массив для хранения уже добавленных сотрудников
existing_ids = []

# Цикл добавления сотрудников
for _ in range(49999):
    full_name = fake.name()
    position = fake.job()
    hire_date = fake.date_between(start_date='-10y', end_date='today')
    salary = round(random.uniform(30000, 150000), 2)

    # Получаем список текущих сотрудников
    cur.execute("SELECT id FROM employees")
    current_employees = cur.fetchall()

    # Извлекаем список уникальных идентификаторов сотрудников
    existing_ids = [row[0] for row in current_employees]

    # Если уже есть сотрудники, случайным образом выбираем руководителя
    if existing_ids:
        manager_id = random.choice(existing_ids)
    else:
        manager_id = None

    # Вставляем нового сотрудника
    cur.execute('''
        INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
        VALUES (%s, %s, %s, %s, %s)
    ''', (full_name, position, hire_date, salary, manager_id))

# Фиксируем изменения
conn.commit()

# Закрываем соединение
cur.close()
conn.close()