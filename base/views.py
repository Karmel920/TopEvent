from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Topic, Message
from .forms import ProjectForm


def login_view(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist!')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_view(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Something went wrong during registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    projects = Project.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()
    project_count = projects.count()
    context = {'projects': projects, 'topics': topics, 'project_count': project_count}
    return render(request, 'base/home.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    comments = project.message_set.all().order_by('-created')
    participants = project.participants.all()

    if request.method == 'POST':
        comment = Message.objects.create(
            user=request.user,
            project=project,
            body=request.POST.get('body')
        )
        project.participants.add(request.user)
        return redirect('project', pk=project.id)

    context = {'project': project, 'comments': comments, 'participants': participants}
    return render(request, 'base/project.html', context)


@login_required(login_url='/login')
def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)


@login_required(login_url='/login')
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)


@login_required(login_url='/login')
def delete_project(request, pk):
    project = Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        return redirect('home')

    context = {'obj': project}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def delete_message(request, pk):
    comment = Message.objects.get(id=pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('home')

    context = {'obj': comment}
    return render(request, 'base/delete.html', context)
