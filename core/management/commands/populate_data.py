from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Role, Department, Employee, Salary, Bonus, EmployeeProfile
from datetime import date, timedelta
import random
from faker import Faker

fake = Faker()

def random_date():
    start_date = date.today() - timedelta(days=5*365)
    days_diff = (date.today() - start_date).days
    return start_date + timedelta(days=random.randint(0, days_diff))

def create_unique_username(first_name, last_name):
    base_username = f"{first_name.lower()}.{last_name.lower()}@company.com"
    username = base_username
    i = 1
    while User.objects.filter(username=username).exists():
        username = f"{first_name.lower()}.{last_name.lower()}{i}@company.com"
        i += 1
    return username

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        if User.objects.exists() or Employee.objects.exists():
            self.stdout.write(self.style.WARNING('Database already populated. Exiting.'))
            return

        roles = ['CEO', 'HR', 'Manager', 'Worker']
        for role_name in roles:
            Role.objects.get_or_create(name=role_name)

        departments = ['Executive', 'Human Resources', 'Software Development', 'Sales & Marketing']
        for dept_name in departments:
            Department.objects.get_or_create(name=dept_name)

        ceo_role = Role.objects.get(name='CEO')
        manager_role = Role.objects.get(name='Manager')
        hr_role = Role.objects.get(name='HR')
        worker_role = Role.objects.get(name='Worker')

        exec_dept = Department.objects.get(name='Executive')
        hr_dept = Department.objects.get(name='Human Resources')
        sd_dept = Department.objects.get(name='Software Development')
        sm_dept = Department.objects.get(name='Sales & Marketing')

        ceo_user = User.objects.create_user(
            username='john.doe@company.com',
            email='john.doe@company.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        ceo = Employee.objects.create(
            user=ceo_user,
            role=ceo_role,
            department=exec_dept,
            manager=None,
            hire_date=random_date()
        )

        hr_manager_user = User.objects.create_user(
            username='jane.smith@company.com',
            email='jane.smith@company.com',
            password='password123',
            first_name='Jane',
            last_name='Smith'
        )
        hr_manager = Employee.objects.create(
            user=hr_manager_user,
            role=manager_role,
            department=hr_dept,
            manager=ceo,
            hire_date=random_date()
        )

        for _ in range(10):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = create_unique_username(first_name, last_name)
            user = User.objects.create_user(
                username=username,
                email=username,
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            Employee.objects.create(
                user=user,
                role=hr_role,
                department=hr_dept,
                manager=hr_manager,
                hire_date=random_date()
            )

        sd_manager_user = User.objects.create_user(
            username='alice.johnson@company.com',
            email='alice.johnson@company.com',
            password='password123',
            first_name='Alice',
            last_name='Johnson'
        )
        sd_manager = Employee.objects.create(
            user=sd_manager_user,
            role=manager_role,
            department=sd_dept,
            manager=ceo,
            hire_date=random_date()
        )

        for _ in range(90):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = create_unique_username(first_name, last_name)
            user = User.objects.create_user(
                username=username,
                email=username,
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            Employee.objects.create(
                user=user,
                role=worker_role,
                department=sd_dept,
                manager=sd_manager,
                hire_date=random_date()
            )

        sm_manager_user = User.objects.create_user(
            username='bob.brown@company.com',
            email='bob.brown@company.com',
            password='password123',
            first_name='Bob',
            last_name='Brown'
        )
        sm_manager = Employee.objects.create(
            user=sm_manager_user,
            role=manager_role,
            department=sm_dept,
            manager=ceo,
            hire_date=random_date()
        )

        for _ in range(96):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = create_unique_username(first_name, last_name)
            user = User.objects.create_user(
                username=username,
                email=username,
                password='password123',
                first_name=first_name,
                last_name=last_name
            )
            Employee.objects.create(
                user=user,
                role=worker_role,
                department=sm_dept,
                manager=sm_manager,
                hire_date=random_date()
            )

        employees = Employee.objects.all()
        for employee in employees:
            salary_amount = {
                'CEO': 200000,
                'Manager': 100000,
                'HR': 80000,
                'Worker': 60000
            }[employee.role.name]
            Salary.objects.create(
                employee=employee,
                base_salary=salary_amount,
                bonus=0,
                effective_date=employee.hire_date
            )

        for employee in employees:
            EmployeeProfile.objects.create(
                employee=employee,
                bio="Lorem ipsum dolor sit amet.",
                linkedin_url=f"https://linkedin.com/in/{employee.user.username.split('@')[0]}"
            )

        bonus_employees = random.sample(list(employees), int(0.2 * len(employees)))
        for employee in bonus_employees:
            Bonus.objects.create(
                employee=employee,
                amount=5000,
                date=employee.hire_date + timedelta(days=random.randint(1, 365)),
                description="Performance bonus"
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with sample data.'))