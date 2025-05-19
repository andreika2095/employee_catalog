# Генерация данных
def generate_data():
    conn = get_connection()
    cur = conn.cursor()

    # Первый сотрудник (CEO)
    first_employee = ('Иван Петров', 'CEO', '2020-01-01', 150000, None)
    cur.execute('''
        INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
        VALUES (%s, %s, %s, %s, %s)
    ''', first_employee)
    conn.commit()

    for _ in range(49999):
        full_name = fake.name()
        position = fake.job()
        hire_date = fake.date_between(start_date='-10y', end_date='today')
        salary = round(random.uniform(30000, 150000), 2)
        cur.execute("SELECT id FROM employees")
        existing_ids = [row[0] for row in cur.fetchall()]
        manager_id = random.choice(existing_ids) if existing_ids else None
        cur.execute('''
            INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
            VALUES (%s, %s, %s, %s, %s)
        ''', (full_name, position, hire_date, salary, manager_id))

    conn.commit()
    cur.close()
    conn.close()

# Pydantic модели
class EmployeeIn(BaseModel):
    full_name: str
    position: str
    hire_date: date
    salary: float
    manager_id: Optional[int] = None

class EmployeeOut(EmployeeIn):
    id: int

# FastAPI приложение
app = FastAPI(title="Employee Catalog API")

@app.get("/employees", response_model=List[EmployeeOut])
def get_employees():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, position, hire_date, salary, manager_id FROM employees LIMIT 100")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [EmployeeOut(id=row[0], full_name=row[1], position=row[2], hire_date=row[3], salary=row[4], manager_id=row[5]) for row in rows]

@app.get("/employee/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, full_name, position, hire_date, salary, manager_id FROM employees WHERE id = %s", (employee_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return EmployeeOut(id=row[0], full_name=row[1], position=row[2], hire_date=row[3], salary=row[4], manager_id=row[5])
    raise HTTPException(status_code=404, detail="Сотрудник не найден")

@app.post("/employee", response_model=EmployeeOut)
def create_employee(employee: EmployeeIn):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
        """,
        (employee.full_name, employee.position, employee.hire_date, employee.salary, employee.manager_id)
    )
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return EmployeeOut(id=new_id, **employee.dict())

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Сотрудник удалён"}

# Выполняется при запуске напрямую
if __name__ == "__main__":
    create_table()
    generate_data()

