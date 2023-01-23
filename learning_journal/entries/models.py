from time import timezone
from django.db import models
from django.utils import timezone

TAG_CHOICES = (
    ('Text', 'TEXT'),
    ('Code snippet', 'CODE SNIPPET'),
    ('Screenshot', 'SCREENSHOT'),
)

# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    text = models.TextField(blank=True)
    tags = models.CharField(max_length=50, choices=TAG_CHOICES, default='Text')

    def __str__(self):
        return f"{self.title} on {self.date}"

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'