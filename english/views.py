from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from users.models import EnglishLessonProfile
from .forms import LessonForm, CardForm
from .models import EnglishLesson, Card
from users.models import Profile, Group
from django.forms import formset_factory
import json

# Create your views here.
def home(request):
    return render(request, 'english/home.html')

def user_lessons(request, username):
    if User.objects.filter(username=username).exists():
        lessons = EnglishLesson.objects.filter(access=request.user.id)
        user_lessons = EnglishLesson.objects.filter(author=request.user)
        groups = Group.objects.filter(users=request.user.id)
        return render(request, 'english/user_lessons.html', {'username':username, 'lessons':lessons, 'groups':groups, 'user_lessons':user_lessons})
    else:
        return redirect('home')

def create_lesson(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = LessonForm(request.POST)
            CardFormSet = formset_factory(CardForm)
            formset = CardFormSet(request.POST)
            if form.is_valid() and formset.is_valid():  
                lesson = EnglishLesson()
                lesson.author = request.user
                lesson.title = form.cleaned_data['title']
                lesson.save()
                for f in formset.forms:
                    data = f.cleaned_data
                    if data and data['text1'] != '' and data['text2'] != '':
                        lesson.cards.create(text1= data['text1'],text2= data['text2'])
                if len(lesson.cards.all()) > 0:
                    lesson.save()
                    lesson.access.add(request.user)

                    for group in form.cleaned_data['groups']:
                        group.lessons_english.add(lesson)
                        for user in group.users.all():
                            lesson.access.add(user)

                    profile = Profile.objects.get(user=request.user)
                    if profile and not lesson in [L.lesson for L in profile.lessons_english.all()]:
                        lesson_profile = EnglishLessonProfile()
                        lesson_profile.lesson = lesson
                        lesson_profile.user = request.user
                        lesson_profile.save()
                        for card in lesson.cards.all():
                            lesson_profile.cards.create(card=card)
                        lesson_profile.save()
                        profile.lessons_english.add(lesson_profile)
                        profile.save()
                        
                    return redirect('lesson-english',lesson_id = lesson.id)
                else:
                    lesson.delete()
            form.fields['groups'].queryset = Group.objects.filter(admins=request.user.id)
        else:
            form = LessonForm()
            form.fields['groups'].queryset = Group.objects.filter(admins=request.user.id)
            CardFormSet = formset_factory(CardForm,extra=1)
            formset = CardFormSet()
        return render(request, 'english/create_lesson.html', {'form':form,'formset':formset})
    else:
        return redirect('login')

def copy_lesson(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if request.user in lesson.access.all():
            if request.method == 'POST':
                form = LessonForm(request.POST)
                CardFormSet = formset_factory(CardForm)
                formset = CardFormSet(request.POST)
                if form.is_valid() and formset.is_valid(): 
                    lesson = EnglishLesson()
                    lesson.author = request.user
                    lesson.title = form.cleaned_data['title']
                    lesson.save()
                    for f in formset.forms:
                        data = f.cleaned_data
                        if data and data['text1'] != '' and data['text2'] != '':
                            lesson.cards.create(text1= data['text1'],text2= data['text2'])
                    if len(lesson.cards.all()) > 0:
                        lesson.save()
                        lesson.access.add(request.user)

                        for group in form.cleaned_data['groups']:
                            group.lessons_english.add(lesson)
                            for user in group.users.all():
                                lesson.access.add(user)

                        profile = Profile.objects.get(user=request.user)
                        if profile and not lesson in [L.lesson for L in profile.lessons_english.all()]:
                            lesson_profile = EnglishLessonProfile()
                            lesson_profile.lesson = lesson
                            lesson_profile.user = request.user
                            lesson_profile.save()
                            for card in lesson.cards.all():
                                lesson_profile.cards.create(card=card)
                            lesson_profile.save()
                            profile.lessons_english.add(lesson_profile)
                            profile.save()
                            
                        return redirect('lesson-english',lesson_id = lesson.id)
            else:
                form = LessonForm({'title':lesson.title})
                form.fields['groups'].queryset = Group.objects.filter(admins=request.user)
                cards = lesson.cards.all()
                CardFormSet = formset_factory(CardForm, extra=0)
                formset = CardFormSet(initial=cards.values())
                return render(request, 'english/create_lesson.html', {'form':form,'formset':formset})
    return redirect('user-lessons-english', username=request.user.username)

def edit_lesson(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if request.user in lesson.access.all():
            groups = Group.objects.filter(admins=request.user, lessons_english=lesson.id)
            profile = Profile.objects.get(user=request.user)
            lesson_profile = profile.lessons_english.get(lesson=lesson.id) 
            if request.method == 'POST':
                form = LessonForm(request.POST)
                CardFormSet = formset_factory(CardForm)
                formset = CardFormSet(request.POST)
                if form.is_valid() and formset.is_valid():
                    lesson.title = form.cleaned_data['title']
                    formset_cards = []
                    for f in formset.forms:
                        data = f.cleaned_data
                        if data and data['text1'] != '' and data['text2'] != '':
                            try:
                                card = lesson.cards.filter(text1=data['text1'],text2=data['text2'])
                                formset_cards.append(card[0])
                            except IndexError:
                                card = Card(text1=data['text1'],text2=data['text2'])
                                card.save()
                                formset_cards.append(card)
                                lesson.cards.add(card)
                                lesson_profile.cards.create(card=card)

                    for card in lesson.cards.all():
                        if not card in formset_cards:
                            card.delete()
                        
                    lesson.save()

                    for group in groups:
                        if not group in form.cleaned_data['groups']:
                            group.lessons_english.remove(lesson)
                            for user in group.users.all():
                                if user != group.super_admin:
                                    lesson.access.remove(user)

                    for group in form.cleaned_data['groups']:
                        for user in group.users.all():
                            lesson.access.add(user)

                    return redirect('lesson-english',lesson_id = lesson.id)
                form.fields['groups'].queryset = Group.objects.filter(admins=request.user.id)
            else:        
                if request.user == lesson.author:
                    form = LessonForm({'title':lesson.title, 'groups':groups})
                    form.fields['groups'].queryset = Group.objects.filter(admins=request.user)
                else:
                    form = LessonForm({'title':lesson.title})
                    form.fields['groups'].queryset = Group.objects.none()
                cards = lesson.cards.all()
                CardFormSet = formset_factory(CardForm, extra=0)
                formset = CardFormSet(initial=cards.values())            
            return render(request, 'english/create_lesson.html', {'form':form,'formset':formset,'lesson':lesson})
        return redirect('home')
    else:
        return redirect('home')
 
def lesson(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if request.user in lesson.access.all():
            profile = Profile.objects.get(user=request.user)
            group = Group.objects.filter(users=request.user.id, lessons_english=lesson.id).first()
            if not lesson in [L.lesson for L in profile.lessons_english.all()]:
                lesson_profile = EnglishLessonProfile()
                lesson_profile.lesson = lesson
                lesson_profile.user = request.user
                lesson_profile.save()
                for card in lesson.cards.all():
                    lesson_profile.cards.create(card=card)
                lesson_profile.save()
                profile.lessons_english.add(lesson_profile)
                profile.save()
            return render(request, 'english/lesson.html', {'lesson':lesson, 'group':group})
    return redirect('user-lessons-english', username=request.user.username)

def lesson_cards(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if request.user in lesson.access.all():
            return render(request, 'english/lesson_cards.html', {'lesson':lesson})
    return redirect('user-lessons-english', username=request.user.username)

def quizz(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if request.method == "POST":
            cards = json.loads(request.POST['cards'])
            key = int(json.loads(request.POST['key'])) + 1
            profile = Profile.objects.get(user=request.user)
            lesson_profile = profile.lessons_english.get(lesson=lesson.id)
            lesson_profile.key = key
            lesson_profile.save()
            for cardData in cards:
                card = lesson.cards.get(text1=cardData['text1'],text2=cardData['text2'])
                cardProfile = lesson_profile.cards.get(card=card.id)
                cardProfile.counter = cardData['counter']
                cardProfile.correct = cardData['correct']
                cardProfile.save()
        profile = Profile.objects.get(user=request.user)
        profile = profile.lessons_english.get(lesson=lesson.id)  
        return render(request, 'english/quizz.html', {'lesson':lesson,'profile':profile})
    return redirect('home')

def training(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        return render(request, 'english/training.html', {'lesson':lesson})
    return redirect('home')

def lesson_share(request, lesson_id, share_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if str(lesson.share_id) == share_id:
            if request.user.is_authenticated:
                lesson.access.add(request.user)
                return redirect('lesson-english', lesson_id = lesson.id)
            return render(request, 'english/lesson.html', {'lesson':lesson})
    return redirect('home')

def delete_lesson(request, lesson_id):
    lesson = EnglishLesson.objects.get(id=lesson_id)
    if lesson:
        if lesson.author == request.user:
            for card in lesson.cards.all():
                card.delete()
            lesson.delete()
            return redirect('user-lessons-english', username=request.user.username)
        return redirect('lesson-english', lesson_id=lesson.id)
    return redirect('home')