from django.shortcuts import render, redirect
from django.db.models import Q
from .models import Project, Topic
from .forms import ProjectForm


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
    context = {'project': project}
    return render(request, 'base/project.html', context)


def create_project(request):
    form = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/project_form.html', context)


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


def delete_project(request, pk):
    project = Project.objects.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('home')
    context = {'obj': project}
    return render(request, 'base/delete.html', context)
