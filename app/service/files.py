from service.file import File

class Jobs(File):
    name = 'jobs'
    columns_name = ['id', 'job']
    path = 'data/jobs.csv'


class Departments(File):
    name = 'departments'
    columns_name = ['id', 'department']
    path = 'data/departments.csv'


class HiredEmployees(File):
    name = 'hired_employees'
    columns_name = ['id', 'name', 'datetime', 'department_id', 'job_id']
    path = 'data/hired_employees.csv'
