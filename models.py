from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class EmployeeIn(BaseModel):
    full_name: str
    position: str
    hire_date: date
    salary: float
    manager_id: Optional[int] = None

class EmployeeOut(EmployeeIn):
    id: int

class EmployeeHierarchy(BaseModel):
    id: int
    full_name: str
    position: str
    subordinates: List["EmployeeHierarchy"] = []

# Для рекурсивных моделей
EmployeeHierarchy.update_forward_refs()