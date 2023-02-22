from time import timezone
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


TAG_CHOICES = (
    ('NOTE','Note'),
    ('CODE SNIPPET','Code snippet'),
    ('SCREENSHOT','Screenshot'),
    ('ACHIEVEMENT','Achievement'),
)

# Create your models here.
class Entry(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=50, choices=TAG_CHOICES, default='Note')

    def __str__(self):
        return f"{self.title} on {self.date}"

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'