from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string

def generate_account_number():
    return 'WLT' + ''.join(random.choices(string.digits, k=9))

class User(AbstractUser):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('rejected', 'Rejected'),
        ('suspended', 'Suspended'),
    ]
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True)
    account_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    upi_id = models.CharField(max_length=100, blank=True)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    id_photo = models.ImageField(upload_to='id_photos/', blank=True, null=True)
    account_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    account_opened = models.BooleanField(default=False)
    admin_note = models.TextField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def save(self, *args, **kwargs):
        if not self.account_number and self.account_opened:
            self.account_number = generate_account_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    class Meta:
        ordering = ['-created_at']
