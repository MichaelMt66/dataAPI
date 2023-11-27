from enum import Enum


class FileName(str, Enum):
    job = "job"
    departments = "departments"
    hired_employees = "hired_employees"
