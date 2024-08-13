from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

# Create your models here.
class Card(models.Model):
    text1 = models.TextField()
    text2 = models.TextField()

    def __str__(self):
        return f'{self.text1} <-> {self.text2}'

class EnglishLesson(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False)
    date = models.DateTimeField(default=datetime.now(), editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_user_english')
    title = models.CharField(max_length=50)
    cards = models.ManyToManyField(Card)
    access = models.ManyToManyField(User, default=author, related_name='access_user_english')

    def __str__(self):
        return self.title