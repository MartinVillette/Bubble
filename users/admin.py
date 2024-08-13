from django.contrib import admin
from .models import Profile, Group, CardProfile, EnglishLessonProfile, QuoteProfile, QuoteTag

# Register your models here.
admin.site.register(Profile)
admin.site.register(Group)
admin.site.register(EnglishLessonProfile)
admin.site.register(CardProfile)
admin.site.register(QuoteProfile)
admin.site.register(QuoteTag)