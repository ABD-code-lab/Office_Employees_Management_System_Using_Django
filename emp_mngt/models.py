from django.db import models
from django.contrib.auth.models import User
from datetime import date

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    def calculate_performance(self):
        # Get all attendance records for this employee
        attendances = Attendance.objects.filter(employee=self)
        if not attendances.exists():
            return 0  # No attendance records, performance is 0

        # Calculate the percentage of days present
        total_days = attendances.count()
        present_days = attendances.filter(status='Present').count()
        performance_percentage = (present_days / total_days) * 100

        return round(performance_percentage, 2)  # Round to 2 decimal places

    def get_performance_stars(self):
        performance = self.calculate_performance()
        # Convert performance percentage to stars (1-5)
        if performance >= 90:
            return "★★★★★"
        elif performance >= 70:
            return "★★★★☆"
        elif performance >= 50:
            return "★★★☆☆"
        elif performance >= 30:
            return "★★☆☆☆"
        else:
            return "★☆☆☆☆"


class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.employee.name} - {self.date} - {self.status}"