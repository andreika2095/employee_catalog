from pydantic import BaseModel
from datetime import date
from typing import Optional

class EmployeeIn(BaseModel):
    full_name: str
    position: str
    hire_date: date
    salary: float
    manager_id: Optional[int] = None

class EmployeeOut(EmployeeIn):
    id: int