from django.db import models
from django.contrib.auth.models import User
import string
import random


def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))

class ShortenedURL(models.Model):
    original_url = models.URLField(max_length=500)
    short_code = models.CharField(max_length=6, unique = True, default=generate_short_code)
    create_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True) # associate with the user
    
    def __str__(self):
        return f"{self.original_url} -> {self.short_code}"
