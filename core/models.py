from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import date

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    hire_date = models.DateField()

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.role}"

    def is_manager(self):
        return self.employee_set.exists()

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salaries')
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_date = models.DateField()

    class Meta:
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.effective_date}"

class Bonus(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='bonuses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"{self.employee.user.get_full_name()} - {self.date} - {self.amount}"

class Hiring(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('interviewed', 'Interviewed'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
    ]
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    application_date = models.DateField(default=date.today)  # Add default
    interview_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    remarks = models.TextField(blank=True)
    employee = models.OneToOneField('Employee', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.status}"

    def clean(self):
        if self.status == 'hired' and not self.employee:
            raise ValidationError("Hired candidates must be linked to an Employee record.")

class EmployeeProfile(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)
    resume_file = models.FileField(upload_to='resumes/', blank=True)
    linkedin_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.employee.user.get_full_name()}"   