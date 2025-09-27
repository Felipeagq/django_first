from django.db import models
from accounts.models import User

# Create your models here.
# -----------------------
# Curso
# -----------------------
class Course(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    file_url = models.URLField(blank=True, null=True)
    published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# -----------------------
# Archivos
# -----------------------
class File(models.Model):
    filename = models.CharField(max_length=500)
    storage_path = models.TextField()  # Puede ser S3, GCS o local path
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    size = models.BigIntegerField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.filename




# -----------------------
# Quiz
# -----------------------
class Quiz(models.Model):
    # section = models.OneToOneField(Section, on_delete=models.CASCADE, related_name="quiz")
    title = models.CharField(max_length=300, blank=True, null=True)
    # time_limit_seconds = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quiz: {self.title or self.section.title}"

# -----------------------
# Secciones
# -----------------------
class Section(models.Model):
    TEXT_IMAGE = "text_image"
    VIDEO = "video"
    QUIZ = "quiz"

    CONTENT_TYPES = [
        (TEXT_IMAGE, "Text & Image"),
        (VIDEO, "Video"),
        (QUIZ, "Quiz"),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=300)
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPES)
    content = models.TextField(blank=True, null=True)  # Texto o URL de video
    # file = models.ForeignKey(File, on_delete=models.SET_NULL, null=True, blank=True)
    file_url = models.URLField(blank=True, null=True)
    position = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    quiz = models.OneToOneField(
        Quiz,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="section"
    )
    class Meta:
        ordering = ["position"]

    def __str__(self):
        return f"{self.course.title} - {self.title}"



# -----------------------
# Preguntas
# -----------------------
class Question(models.Model):
    MULTIPLE_CHOICE = "multiple_choice"
    CHECKBOX = "checkbox"
    OPEN = "open"

    QUESTION_TYPES = [
        (MULTIPLE_CHOICE, "Multiple Choice"),
        (CHECKBOX, "Checkbox"),
        (OPEN, "Open Answer"),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPES, default=MULTIPLE_CHOICE)
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position"]

    def __str__(self):
        return self.question_text


# -----------------------
# Opciones de respuesta
# -----------------------
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_text} ({'Correct' if self.is_correct else 'Wrong'})"


# -----------------------
# Intentos de quiz
# -----------------------
class Attempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="attempts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    score = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Attempt by {self.user} on {self.quiz}"


# -----------------------
# Respuestas
# -----------------------
class Answer(models.Model):
    attempt = models.ForeignKey(Attempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="answers")
    answer_value = models.TextField(blank=True, null=True)  # texto o JSON
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} - {self.question}"
