from rest_framework import serializers
from .models import (
    Course, Section, Quiz,
    Question,Answer,Choice
)
import boto3
from django.conf import settings

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ("id","title")
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ("__all__")
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ("__all__")
class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'choice_text', 'is_correct']
class QuestionDetailSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'position', 'choices']
class QuizDetailSerializer(serializers.ModelSerializer):
    questions = QuestionDetailSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'created_at', 'questions']


class SectionSerializer(serializers.ModelSerializer):
    quizzes = QuizSerializer(many=True, read_only=True)
    quiz_id = serializers.PrimaryKeyRelatedField(
        source="quiz",  # apunta a la relación
        read_only=True
    )
    file = serializers.FileField(write_only=True, required=False)
    class Meta:
        model = Section
        fields = ["id", "title", "content_type", "content", "position", "quiz_id", "quizzes",'file',"file_url","course"]
        read_only_fields = ['file_url']
    def create(self, validated_data):
        file = validated_data.pop("file", None)
        section = Section.objects.create(**validated_data)

        if file:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            file_key = f"sections/{file.name}"
            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_key)

            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
            section.file_url = file_url
            section.save()

        return section
        
        


class CourseSerializer(serializers.ModelSerializer):
    file = serializers.FileField(write_only=True, required=False)
    class Meta:
        model = Course
        fields = ('id','description', 'price', 'published','title','file','file_url')
        read_only_fields = ['file_url']
    def create(self, validated_data):
        file = validated_data.pop("file", None)
        section = Course.objects.create(**validated_data)

        if file:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME
            )

            file_key = f"sections/{file.name}"
            s3.upload_fileobj(file, settings.AWS_STORAGE_BUCKET_NAME, file_key)

            file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{file_key}"
            section.file_url = file_url
            section.save()

        return section


class CourseDetailSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Course
        fields = ('__all__')