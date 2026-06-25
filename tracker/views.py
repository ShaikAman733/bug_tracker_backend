pythonfrom rest_framework.views import APIView
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import User, Project, Bug
from .serializers import UserSerializer, ProjectSerializer, BugSerializer
class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
class DeveloperViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(role='DEVELOPER')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], url_path='status')
    def update_status(self, request, pk=None):
        bug = self.get_object()
        new_status = request.data.get('status')
        resolution_comment = request.data.get('resolution_comment', bug.resolution_comment)

        if new_status:
            bug.status = new_status
            bug.resolution_comment = resolution_comment
            bug.save()
            return Response({'status': 'Bug status updated', 'current_status': bug.status})
        
        return Response({'error': 'Status not provided'}, status=status.HTTP_400_BAD_REQUEST)