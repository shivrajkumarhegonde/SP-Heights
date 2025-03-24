from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('flat_owner', 'Flat Owner'),
        ('tenant', 'Tenant'),
    ]

    phone_number = models.CharField(max_length=15)
    flat_number = models.CharField(max_length=10)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='flat_owner')
    is_admin = models.BooleanField(default=False)
    is_flat_owner = models.BooleanField(default=False)
    is_tenant = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Role(models.Model):
    ROLE_TYPES = [
        ('admin', 'Admin'),
        ('flat_owner', 'Flat Owner'),
        ('tenant', 'Tenant'),
    ]
    role_type = models.CharField(max_length=20, choices=ROLE_TYPES, unique=True)

    def __str__(self):
        return self.role_type

class Notice(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.title

class Flat(models.Model):
    flat_number = models.CharField(max_length=10, unique=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_flats')
    tenant = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='rented_flats')

    def __str__(self):
        return self.flat_number

class MaintenanceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)  # ✅ Add this to avoid the error

    def __str__(self):
        return self.title



# Membership Directory
ROLE_CHOICES = (
    ('chairman', 'Chairman'),
    ('treasurer', 'Treasurer'),
    ('admin', 'admin'),
    ('tenant', 'Tenant'),
    ('flat_owner', 'Flat Owner'),
    ('secretary', 'Secretary'),



)

class Member(models.Model):
    name = models.CharField(max_length=100)  # Default name for existing records
    phone_number = models.CharField(max_length=15)
    flat_number = models.CharField(max_length=10, unique=True)  # Ensure uniqueness
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    email = models.EmailField()
    address = models.TextField()

    def __str__(self):
        return self.name