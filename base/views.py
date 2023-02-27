from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Topic, Message, UserDetails
from .forms import ProjectForm, UserForm, UserDetailsForm, UserDetailsCreationForm


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
    user = request.user
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('register-details')
        else:
            messages.error(request, 'Something went wrong during registration')

    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def create_user_details(request):
    form = UserDetailsCreationForm()
    if request.method == 'POST':
        user = request.user
        UserDetails.objects.create(
            user=user,
            name=request.POST.get('name'),
            email=request.POST.get('email')
        )
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/register_details.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    projects = Project.objects.filter(
        Q(topic__name__contains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    all_projects = Project.objects.all()
    topics = Topic.objects.all()[:5]
    project_count = projects.count()
    comments = Message.objects.filter(Q(project__topic__name__icontains=q))

    context = {'projects': projects, 'topics': topics, 'project_count': project_count, 'comments': comments,
               'all_projects': all_projects}
    return render(request, 'base/home.html', context)


def project(request, pk):
    project = Project.objects.get(id=pk)
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    comments = project.message_set.all()
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


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    projects = user.project_set.all()
    all_projects = Project.objects.all()
    comments = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'projects': projects, 'comments': comments, 'topics': topics,
               'all_projects': all_projects}
    return render(request, 'base/profile.html', context)


@login_required(login_url='/login')
def create_project(request):
    form = ProjectForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Project.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/project_form.html', context)


@login_required(login_url='/login')
def update_project(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        project.name = request.POST.get('name')
        project.topic = topic
        project.description = request.POST.get('description')
        project.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'project': project}
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
        return redirect('project', pk=comment.project.id)

    context = {'obj': comment}
    return render(request, 'base/delete.html', context)


@login_required(login_url='/login')
def update_user(request):
    user = request.user
    form = UserDetailsForm(instance=user.userdetails)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST, request.FILES, instance=user.userdetails)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update-user.html', context)


def topics_view(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics': topics}
    return render(request, 'base/topics.html', context)


def activity_view(request):
    comments = Message.objects.all()
    context = {'comments': comments}
    return render(request, 'base/activity.html', context)
