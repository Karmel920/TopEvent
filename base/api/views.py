from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Project
from .serializers import ProjectSerializer


@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/projects',
        'GET /api/projects/:id'
    ]
    return Response(routes)


@api_view(['GET'])
def get_projects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_project(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
