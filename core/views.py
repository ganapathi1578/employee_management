from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Employee, EmployeeProfile, Department, Hiring
from .forms import EmployeeProfileForm, HiringForm, EmployeeCreationForm

def home(request):
    return render(request, 'core/home.html')

def register_view(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')  # Make sure 'login' is in your `urls.py` or update to your actual login path name
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EmployeeCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def profile(request):
    employee = request.user.employee
    profile, created = EmployeeProfile.objects.get_or_create(employee=employee)
    if request.method == 'POST':
        form = EmployeeProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:profile')
    else:
        form = EmployeeProfileForm(instance=profile)
    return render(request, 'core/profile.html', {'employee': employee, 'form': form})

def role_required(role_name):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if hasattr(request.user, 'employee') and request.user.employee.role.name == role_name:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return wrapper
    return decorator

@login_required
@role_required('HR')
def hr_view(request):
    employees = Employee.objects.all()
    return render(request, 'core/hr_view.html', {'employees': employees})

@login_required
@role_required('CEO')
def ceo_view(request):
    departments = Department.objects.all()
    employee_count = Employee.objects.count()
    recent_hires = Employee.objects.order_by('-hire_date')[:5]
    return render(request, 'core/ceo_view.html', {
        'departments': departments,
        'employee_count': employee_count,
        'recent_hires': recent_hires,
    })

@login_required
def manager_view(request):
    direct_reports = Employee.objects.filter(manager=request.user.employee)
    if not direct_reports.exists():
        raise PermissionDenied
    return render(request, 'core/manager_view.html', {'direct_reports': direct_reports})

@login_required
@role_required('HR')
def hiring_list(request):
    hirings = Hiring.objects.all()
    return render(request, 'core/hiring_list.html', {'hirings': hirings})

@login_required
@role_required('HR')
def hiring_create(request):
    if request.method == 'POST':
        form = HiringForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:hiring_list')
    else:
        form = HiringForm()
    return render(request, 'core/hiring_form.html', {'form': form})

@login_required
@role_required('HR')
def hiring_update(request, pk):
    hiring = get_object_or_404(Hiring, pk=pk)
    if request.method == 'POST':
        form = HiringForm(request.POST, instance=hiring)
        if form.is_valid():
            form.save()
            if form.cleaned_data['status'] == 'hired' and not hiring.employee:
                return redirect('core:onboard_employee', hiring_id=hiring.id)
            return redirect('core:hiring_list')
    else:
        form = HiringForm(instance=hiring)
    return render(request, 'core/hiring_form.html', {'form': form})

@login_required
@role_required('HR')
def onboard_employee(request, hiring_id):
    hiring = get_object_or_404(Hiring, id=hiring_id)
    if hiring.status != 'hired' or hiring.employee:
        return redirect('core:hiring_list')
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            employee = Employee.objects.get(user=user)
            hiring.employee = employee
            hiring.save()
            return redirect('core:hiring_list')
    else:
        initial_data = {
            'first_name': hiring.first_name,
            'last_name': hiring.last_name,
            'email': hiring.email,
        }
        form = EmployeeCreationForm(initial=initial_data)
    return render(request, 'core/onboard_employee.html', {'form': form, 'hiring': hiring})

@login_required
@role_required('HR')
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('core:hr_view')
    else:
        form = EmployeeCreationForm()
    return render(request, 'core/onboard_employee.html', {'form': form})