from django.urls import path
from .views import (
    AdminOnlyView, StudentOnlyView, TeacherOnlyView,
    CourseViewSet,SectionViewSet, QuizViewSet, list_courses_public
)
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("admin/", AdminOnlyView.as_view()),
    path("student/", StudentOnlyView.as_view()),
    path("teacher/", TeacherOnlyView.as_view()),
    path("public/", list_courses_public, name="public"),
    
]

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'sections', SectionViewSet, basename='sections')
router.register(r'quiz', QuizViewSet, basename='quiz')

urlpatterns += router.urls