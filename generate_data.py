from faker import Faker
import random
from database import get_connection

def generate_data():
    fake = Faker('ru_RU')
    Faker.seed(4321)
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Уровень 1: CEO
            cur.execute('''
                INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', ('Иван Петров', 'CEO', '2020-01-01', 150000, None))
            ceo_id = cur.fetchone()['id']
            conn.commit()

            # Уровень 2: 9 менеджеров
            level2_ids = []
            for _ in range(9):
                cur.execute('''
                    INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                ''', (
                    fake.name(),
                    fake.job(),
                    fake.date_between(start_date='-10y', end_date='today'),
                    round(random.uniform(50000, 100000), 2),
                    ceo_id
                ))
                level2_ids.append(cur.fetchone()['id'])
            conn.commit()

            # Уровень 3: 90 сотрудников (по 10 на менеджера уровня 2)
            level3_ids = []
            for manager_id in level2_ids:
                for _ in range(10):
                    cur.execute('''
                        INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    ''', (
                        fake.name(),
                        fake.job(),
                        fake.date_between(start_date='-9y', end_date='today'),
                        round(random.uniform(40000, 90000), 2),
                        manager_id
                    ))
                    level3_ids.append(cur.fetchone()['id'])
            conn.commit()

            # Уровень 4: 900 сотрудников (по 10 на менеджера уровня 3)
            level4_ids = []
            for manager_id in level3_ids:
                for _ in range(10):
                    cur.execute('''
                        INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    ''', (
                        fake.name(),
                        fake.job(),
                        fake.date_between(start_date='-8y', end_date='today'),
                        round(random.uniform(30000, 80000), 2),
                        manager_id
                    ))
                    level4_ids.append(cur.fetchone()['id'])
            conn.commit()

            # Уровень 5: 49000 сотрудников (случайное распределение по менеджерам уровня 4)
            total_level5 = 49000
            batch_size = 1000
            for i in range(0, total_level5, batch_size):
                batch = []
                current_batch = min(batch_size, total_level5 - i)
                for _ in range(current_batch):
                    manager_id = random.choice(level4_ids)
                    batch.append((
                        fake.name(),
                        fake.job(),
                        fake.date_between(start_date='-7y', end_date='today'),
                        round(random.uniform(30000, 70000), 2),
                        manager_id
                    ))
                cur.executemany('''
                    INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                    VALUES (%s, %s, %s, %s, %s)
                ''', batch)
                conn.commit()
                print(f"Сгенерировано {i + current_batch}/{total_level5} сотрудников уровня 5")

if __name__ == "__main__":
    generate_data()