from fastapi import FastAPI, HTTPException
from database import get_connection
from models import EmployeeIn, EmployeeOut, EmployeeHierarchy
import uvicorn

app = FastAPI(title="Employee Catalog API")

@app.on_event("startup")
async def startup_event():
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
                tuple(employee.dict().values())
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

@app.get("/employees/hierarchy", response_model=EmployeeHierarchy)
def get_employees_hierarchy():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, full_name, position, manager_id FROM employees")
            employees = cur.fetchall()
    
    if not employees:
        raise HTTPException(status_code=404, detail="Сотрудники не найдены")
    
    # Построение словаря для быстрого доступа к подчиненным
    manager_map = {}
    for emp in employees:
        emp_dict = dict(emp)
        manager_id = emp_dict['manager_id']
        if manager_id not in manager_map:
            manager_map[manager_id] = []
        manager_map[manager_id].append(emp_dict)
    
    # Рекурсивная функция построения дерева
    def build_tree(manager_id):
        nodes = []
        for emp in manager_map.get(manager_id, []):
            node = {
                "id": emp["id"],
                "full_name": emp["full_name"],
                "position": emp["position"],
                "subordinates": build_tree(emp["id"])
            }
            nodes.append(node)
        return nodes
    
    # Находим корневой элемент (CEO)
    root_list = manager_map.get(None, [])
    if not root_list:
        raise HTTPException(status_code=500, detail="CEO не найден")
    
    root_emp = root_list[0]
    return {
        "id": root_emp["id"],
        "full_name": root_emp["full_name"],
        "position": root_emp["position"],
        "subordinates": build_tree(root_emp["id"])
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)