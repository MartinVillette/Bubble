from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, GroupForm
from .models import Group
from django.contrib.auth.models import User
import json 
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Vous avez bien été inscrit')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form':form})

def login_redirect(request):
    if request.user.is_authenticated:
        return redirect('home')

def groups(request):
    if request.user.is_authenticated:
        groups = Group.objects.filter(users=request.user.id)
        admin_groups = []
        users_groups = []
        for group in groups:
            if request.user in group.admins.all():
                admin_groups.append(group)
            else:
                users_groups.append(group)
        return render(request, 'users/groups.html', {'admin_groups':admin_groups, 'users_groups':users_groups})
    return redirect('home')

def create_group(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = GroupForm(request.POST)
            if form.is_valid():
                group = Group()
                group.name = form.cleaned_data['name']
                group.super_admin = request.user
                group.save()
                group.admins.add(request.user)
                group.users.add(request.user)
                group.save()
                return redirect('group-page', group_id=group.id)
        else:
            form = GroupForm()
            return render(request, 'users/create_group.html', {'form':form})
    return redirect('home')

def group_page(request, group_id):
    group = Group.objects.get(id=group_id)
    if group:            
        return render(request, 'users/group_page.html', {'group':group})
    return redirect('home')

def group_share(request, group_id, share_id):
    group = Group.objects.get(id=group_id)
    if group:
        if str(group.share_id) == share_id:
            if request.user.is_authenticated:
                group.users.add(request.user)
                for lesson in group.lessons_english.all():
                    lesson.access.add(request.user)
                return redirect('group-page', group_id = group.id)
            return redirect('groups')
    return redirect('home')

def delete_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if group:
        if group.super_admin == request.user:
            group.delete()
            return redirect('groups')
        return redirect('group', group_id=group.id)
    return redirect('home')

def quit_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if group:
        if request.user in group.users.all():
            group.users.remove(request.user)
        if request.user in group.admins.all():
            group.admins.remove(request.user)
        return redirect('groups')
    return redirect('home')

def edit_group(request, group_id):
    group = Group.objects.get(id=group_id)
    if group:
        if request.user == group.super_admin:
            if request.method == "POST":
                form = GroupForm(request.POST)
                if form.is_valid():
                    group.name = form.cleaned_data['name']
                    group.save()
                    return redirect('group-page', group_id=group.id)
            else:
                form = GroupForm({'name':group.name})
                return render(request, 'users/create_group.html', {'form':form,'group':group})
    return redirect('groups')


def edit_group_users(request, group_id):
    group = Group.objects.get(id=group_id)
    if group:
        if request.method == 'POST':
            admins = request.POST['admins'].split(',')
            admins.append(group.super_admin.username)
            users = request.POST['users'].split(',') + admins
            for user in group.users.all():
                if not user.username in users:
                    group.users.remove(user)
            for admin in group.admins.all():
                if not admin.username in admins:
                    group.admins.remove(admin)

                
            for admin in admins:
                admin = User.objects.get(username=admin)
                if not admin in group.admins.all() and admin in group.users.all():
                    group.admins.add(admin)

            return redirect('group-page', group_id=group.id)
    return redirect('home')

def group_members(request, group_id):
    group = Group.objects.get(id=group_id)
    if group: 
        if request.method == 'POST':
            admins = json.loads(request.POST['admins'])
            users = json.loads(request.POST['users'])
            admins.append(group.super_admin.username)
            users.append(group.super_admin.username)
            for user in group.users.all():
                if not user.username in users:
                    group.users.remove(user)
            for admin in group.admins.all():
                if not admin.username in admins:
                    group.admins.remove(admin)

                
            for admin in admins:
                admin = User.objects.get(username=admin)
                if not admin in group.admins.all() and admin in group.users.all():
                    group.admins.add(admin)

            return redirect('group-page', group_id=group.id)
        elif request.user in group.users.all():
            admins = []
            users = []
            for user in group.users.all():
                if user in group.admins.all():
                    admins.append(user)
                else:
                    users.append(user)
            return render(request, 'users/group_members.html', {'group':group,'admins':admins,'users':users})
    return redirect('groups')

@login_required
def profile(request):
    return render(request, 'users/profile.html')