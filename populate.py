from mimesis import Person
from mimesis.locales import Locale
from random import randint, choice
from datetime import datetime, timedelta
from models import Employee, Base
from db import engine, session

Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

person = Person(Locale.RU)
positions = [
    ('CEO', 1),
    ('Manager', 5),
    ('Team Lead', 20),
    ('Senior Developer', 500),
    ('Developer', 49474),
]

employees = []
manager_ids = []

id_counter = 1
for title, count in positions:
    for _ in range(count):
        name = person.full_name()
        hire_date = person.date(start=2005, end=2024)
        salary = round(randint(50000, 500000), 2)

        if title == 'CEO':
            manager_id = None
        else:
            manager_id = choice(manager_ids)

        emp = Employee(
            id=id_counter,
            full_name=name,
            position=title,
            hire_date=hire_date,
            salary=salary,
            manager_id=manager_id
        )
        employees.append(emp)
        manager_ids.append(id_counter)
        id_counter += 1

session.bulk_save_objects(employees)
session.commit()
print("База данных успешно заполнена 50 000 сотрудниками.")
