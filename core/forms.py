from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeProfile, Hiring, Employee, Role, Department

class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfile
        fields = ['bio', 'profile_picture', 'resume_file', 'linkedin_url']

class HiringForm(forms.ModelForm):
    class Meta:
        model = Hiring
        fields = ['first_name', 'last_name', 'email', 'application_date', 'interview_date', 'status', 'remarks']
        widgets = {
            'application_date': forms.DateInput(attrs={'type': 'date'}),
            'interview_date': forms.DateInput(attrs={'type': 'date'}),
        }

class EmployeeCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True)
    manager = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False)
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'role', 'department', 'manager', 'hire_date']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Employee.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                department=self.cleaned_data['department'],
                manager=self.cleaned_data['manager'],
                hire_date=self.cleaned_data['hire_date']
            )
        return user