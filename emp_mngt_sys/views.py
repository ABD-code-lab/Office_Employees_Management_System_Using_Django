from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from emp_mngt.models import *

def home(req):
    return render(req, 'home.html')

def add_emp(req):
    if req.method == 'POST':
        emp_name = req.POST.get('name')
        email = req.POST.get('email')
        position = req.POST.get('position')
        department = req.POST.get('department')
        salary = req.POST.get('salary')

        x = Employee.objects.create(name=emp_name, 
                                email=email,
                                position=position,
                                department=department,
                                salary=salary)
        x.save()
        return redirect('home')

    return render(req, 'add_employee.html')

def display_emp(req):
    Employees = Employee.objects.all()
    return render(req, 'display_employees.html', {'employees': Employees})

def delete_emp(req):
    if req.method == 'GET':
        emp_id = req.GET.get('id')  
        Employee.objects.filter(id=emp_id).delete() 
    
        return redirect('display_emp') 

def update_emp(request):
    if request.method == 'POST':
        emp_id = request.POST.get('id')
        Employee_instance = Employee.objects.filter(id=emp_id).first()

        if not Employee_instance:
            messages.error(request, "Employee not found.")
            return redirect('display_emp')

        emp_name = request.POST.get('name')
        emp_email = request.POST.get('email')
        emp_position = request.POST.get('position')
        emp_department = request.POST.get('department')
        emp_salary = request.POST.get('salary')

        Employee_instance.name = emp_name
        Employee_instance.email = emp_email
        Employee_instance.position = emp_position
        Employee_instance.department = emp_department
        Employee_instance.salary = emp_salary

        try:
            Employee_instance.save()
            messages.success(request, "Employee updated successfully.")
        except Exception as e:
            messages.error(request, f"Error updating Employee: {str(e)}")

        return redirect('display_emp')

    elif request.method == 'GET':
        emp_id = request.GET.get('id')
        Employee_instance = Employee.objects.filter(id=emp_id).first()

        if not Employee_instance:
            messages.error(request, "Employee not found.")
            return redirect('display_emp')

        return render(request, 'update_Employee.html', {'employee': Employee_instance})

    return redirect('display_emp')

def signup(req):
    if req.method == 'POST':
        name = req.POST.get('fullname')
        email = req.POST.get('email')
        password = req.POST.get('password')
        dob = req.POST.get('dob')

        # Check if user already exists
        if User.objects.filter(username=email).exists():
            messages.error(req, "An account with this email already exists.")
            return redirect('signup')

        # Create a new user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name  # Store the full name in the first_name field
        user.save()

        messages.success(req, "Account created successfully! Please log in.")
        return redirect('signin')

    return render(req, 'signup.html')

def signin(req):
    if req.method == 'POST':
        email = req.POST.get('email')
        password = req.POST.get('password')

        # Authenticate the user
        user = authenticate(username=email, password=password)

        if user is not None:
            login(req, user)
            return redirect('/')  # Redirect to the dashboard
        else:
            messages.error(req, "Invalid email or password.")
            return redirect('signin')

    return render(req, 'signin.html')

def mark_attendance(request):
    employees = Employee.objects.all()

    if request.method == 'POST':
        emp_id = request.POST.get('employee_id')
        status = request.POST.get('status')

        try:
            employee = Employee.objects.get(id=emp_id)  # Ensure employee exists
            Attendance.objects.create(employee=employee, status=status)
            messages.success(request, f"Attendance marked for {employee.name} as {status}.")
            return redirect('view_attendance')
        except Employee.DoesNotExist:
            messages.error(request, "Selected employee does not exist.")
            return redirect('mark_attendance')

    return render(request, 'mark_attendance.html', {'employees': employees})


def view_attendance(request):
    attendances = Attendance.objects.all().order_by('-date')
    employees = Employee.objects.all()

    # Add performance data to each employee
    employee_performance = []
    for employee in employees:
        performance_stars = employee.get_performance_stars()
        employee_performance.append({
            'employee': employee,
            'performance_stars': performance_stars,
        })

    return render(request, 'view_attendance.html', {
        'attendances': attendances,
        'employee_performance': employee_performance,
    })