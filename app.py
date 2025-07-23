from fastapi import FastAPI, HTTPException
from database import get_connection
from models import EmployeeIn, EmployeeOut
import uvicorn

app = FastAPI(title="Employee Catalog API")

@app.on_event("startup")
async def startup_event():
    # Создаем таблицу при запуске приложения
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS employees (
                    id SERIAL PRIMARY KEY,
                    full_name VARCHAR(100),
                    position VARCHAR(100),
                    hire_date DATE,
                    salary NUMERIC(10,2),
                    manager_id INTEGER REFERENCES employees(id)
                )
            ''')
            conn.commit()

@app.get("/employees", response_model=list[EmployeeOut])
def get_employees():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees LIMIT 100")
            return [EmployeeOut(**dict(row)) for row in cur.fetchall()]

@app.get("/employee/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
            row = cur.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return EmployeeOut(**dict(row))

@app.post("/employee", response_model=EmployeeOut)
def create_employee(employee: EmployeeIn):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO employees (full_name, position, hire_date, salary, manager_id)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING *
                """,
                employee.dict().values()
            )
            new_employee = cur.fetchone()
            conn.commit()
    return EmployeeOut(**dict(new_employee))

@app.delete("/employee/{employee_id}")
def delete_employee(employee_id: int):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM employees WHERE id = %s", (employee_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Сотрудник не найден")
            conn.commit()
    return {"message": "Сотрудник удалён"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)