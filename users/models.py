from django.db import models
from django.contrib.auth.models import User
from english.models import EnglishLesson, Card
from french.models import Quote
import uuid

# Create your models here.

class CardProfile(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    counter = models.IntegerField(default=0)
    correct = models.IntegerField(default=0)

class EnglishLessonProfile(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(EnglishLesson, on_delete=models.CASCADE)
    cards = models.ManyToManyField(CardProfile)
    key = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.lesson}'

class QuoteTag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tag = models.TextField()

    def __str__(self):
        return f'{self.tag} by {self.user}'

class QuoteProfile(models.Model):
    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tags = models.ManyToManyField(QuoteTag, blank=True)
    counter = models.IntegerField(default=0)
    active = models.BooleanField(default=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    lessons_english = models.ManyToManyField(EnglishLessonProfile, blank=True)
    quotes = models.ManyToManyField(QuoteProfile, blank=True)

    def __str__(self):
        return str(self.user)

class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, blank=True)
    super_admin = models.ForeignKey(User, on_delete=models.CASCADE)
    admins = models.ManyToManyField(User, related_name='%(class)s_admin')
    users = models.ManyToManyField(User, related_name='%(class)s_users')
    lessons_english = models.ManyToManyField(EnglishLesson, blank=True)
    quotes = models.ManyToManyField(Quote, blank=True)
    share_id = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'{self.name} by {self.super_admin}'