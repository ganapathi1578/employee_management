from django.contrib import admin
from .models import Role, Department, Employee, Salary, Bonus, Hiring, EmployeeProfile

# Show all fields dynamically
def get_all_fields(model):
    return [field.name for field in model._meta.fields]

class EmployeeInline(admin.TabularInline):  # You can use StackedInline for a vertical layout
    model = Employee
    extra = 0  # No extra empty forms
    fields = ['user', 'department', 'hire_date']  # Show relevant fields
    readonly_fields = ['user', 'department', 'hire_date']  # Prevent editing here (optional)
    show_change_link = True  # Allows clicking to view/edit Employee

# Role admin showing related employees inline
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [EmployeeInline]

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [EmployeeInline]

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['user_link', 'role', 'department', 'manager_link', 'hire_date']
    list_filter = ['role', 'department']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    def user_link(self, obj):
        return f'<a href="/admin/app_name/employee/{obj.id}/change/">{obj.user.get_full_name()}</a>'
    user_link.allow_tags = True
    user_link.short_description = 'Employee'

    def manager_link(self, obj):
        if obj.manager:
            return f'<a href="/admin/app_name/employee/{obj.manager.id}/change/">{obj.manager.user.get_full_name()}</a>'
        return '-'
    manager_link.allow_tags = True
    manager_link.short_description = 'Manager'

class SalaryAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Salary)

class BonusAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Bonus)

class HiringAdmin(admin.ModelAdmin):
    list_display = get_all_fields(Hiring)

class EmployeeProfileAdmin(admin.ModelAdmin):
    list_display = get_all_fields(EmployeeProfile)

# Register everything with full field displays
admin.site.register(Role, RoleAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(Bonus, BonusAdmin)
admin.site.register(Hiring, HiringAdmin)
admin.site.register(EmployeeProfile, EmployeeProfileAdmin)

