from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    OCCUPATION_CHOICES = [
        ('farmer', 'Farmer'),
        ('student', 'Student'),
        ('senior_citizen', 'Senior Citizen'),
        ('entrepreneur', 'Entrepreneur'),
        ('small_business_owner', 'Small Business Owner'),
        ('working_professional', 'Working Professional'),
        ('general_public', 'General Public'),
        ('other', 'Other'),
    ]

    INCOME_CHOICES = [
        ('below_1l', 'Below ₹1,00,000'),
        ('1l_to_2.5l', '₹1,00,000 - ₹2,50,000'),
        ('2.5l_to_5l', '₹2,50,000 - ₹5,00,000'),
        ('5l_to_10l', '₹5,00,000 - ₹10,00,000'),
        ('above_10l', 'Above ₹10,00,000'),
    ]

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('te', 'Telugu (తెలుగు)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    state = models.CharField(max_length=100, default='Andhra Pradesh')
    district = models.CharField(max_length=100, blank=True, default='')
    age = models.PositiveIntegerField(null=True, blank=True)
    occupation = models.CharField(max_length=50, choices=OCCUPATION_CHOICES, default='general_public')
    income_range = models.CharField(max_length=50, choices=INCOME_CHOICES, blank=True, default='')
    preferred_language = models.CharField(max_length=10, choices=LANGUAGE_CHOICES, default='en')
    user_interests = models.TextField(blank=True, default='', help_text='Comma-separated or JSON list of interests')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} ({self.get_occupation_display()}, {self.state})"
