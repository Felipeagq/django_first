from rest_framework.views import APIView
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin, IsStudent, IsTeacher
from rest_framework.decorators import api_view,authentication_classes,permission_classes

from .models import Course,Section, Quiz
from .serializers import (
    CourseSerializer, CourseDetailSerializer, SectionSerializer,
    QuizSerializer,QuizDetailSerializer
)

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        return Response({"msg": "Hola Admin!"})

class StudentOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]
    def get(self, request):
        return Response({"msg": "Hola Estudiante!"})

class TeacherOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    def get(self, request):
        return Response({"msg": "Hola Profesor!"})

# class CourseListView(generics.ListAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer

# class CourseDetailView(generics.RetrieveAPIView):
#     queryset = Course.objects.all()
#     serializer_class = CourseDetailSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    def get_serializer_class(self):
        if self.action == "retrieve":  # cuando es detalle
            return QuizDetailSerializer
        return QuizSerializer 

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    # Si quieres usar un serializer distinto para listar y para detalle
    def get_serializer_class(self):
        if self.action == "retrieve":  # cuando es detalle
            return CourseDetailSerializer
        return CourseSerializer  # cuando es lista o create/update/delete

@api_view(["GET"])
@authentication_classes([])  # 👈 vacío = sin autenticación
@permission_classes([])
def list_courses_public(request):
    courses = Course.objects.all()
    serializer_courses = CourseSerializer(courses,many=True)
    return Response(serializer_courses.data)