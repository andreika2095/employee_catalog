from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True)
    full_name = Column(String)
    position = Column(String)
    hire_date = Column(Date)
    salary = Column(Float)
    manager_id = Column(Integer, ForeignKey('employees.id'), nullable=True)

    manager = relationship('Employee', remote_side=[id], backref='subordinates')
