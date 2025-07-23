from faker import Faker
import random
from database import get_connection

def generate_data():
    fake = Faker('ru_RU')
    Faker.seed(4321)
    
    with get_connection() as conn:
        with conn.cursor() as cur:
            # Первый сотрудник (CEO)
            cur.execute('''
                INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            ''', ('Иван Петров', 'CEO', '2020-01-01', 150000, None))
            first_id = cur.fetchone()[0]
            existing_ids = [first_id]
            conn.commit()

            # Генерация 49999 сотрудников
            batch_size = 1000
            total = 49999
            
            for i in range(0, total, batch_size):
                batch = []
                current_batch = min(batch_size, total - i)
                
                for _ in range(current_batch):
                    batch.append((
                        fake.name(),
                        fake.job(),
                        fake.date_between(start_date='-10y', end_date='today'),
                        round(random.uniform(30000, 150000), 2),
                        random.choice(existing_ids)
                    ))
                
                # Пакетная вставка
                cur.executemany('''
                    INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                ''', batch)
                
                # Обновляем список ID
                new_ids = [row[0] for row in cur.fetchall()]
                existing_ids.extend(new_ids)
                conn.commit()
                print(f"Сгенерировано {i + current_batch}/{total} сотрудников")

if __name__ == "__main__":
    generate_data()