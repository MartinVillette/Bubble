from os import access
from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Quote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    AUTHOR = [
        ('Virgile', 'Virgile'),
        ('Simone Weil', 'Simone Weil'),
        ('Michel Vinaver', 'Michel Vinaver'),
    ]
    admin = models.ForeignKey(User, on_delete=models.CASCADE)
    access = models.ManyToManyField(User, related_name='access_user_french')
    author = models.CharField(max_length=20,choices=AUTHOR)
    quote = models.TextField()
    page = models.CharField(max_length=20,blank=True, null=True)

    def __str__(self):
        return f'{self.author} - p.{self.page}' if self.page else f'{self.author}'