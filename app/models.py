from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    # Only for employees – who is their manager
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, limit_choices_to={'role': 'manager'}, related_name='team_members')

    def __str__(self):
        return f"{self.username} ({self.role})"


class Feedback(models.Model):
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    )

    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_received', limit_choices_to={'role': 'employee'})
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_given', limit_choices_to={'role': 'manager'})
    strengths = models.TextField()
    improvement_areas = models.TextField()
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    acknowledged = models.BooleanField(default=False)

    def __str__(self):
        return f"Feedback for {self.employee.username} by {self.manager.username}"
