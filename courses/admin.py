from django.contrib import admin
from .models import (
    Answer,Attempt,Choice,Course,File,
    Question,Quiz,Section
)

# Register your models here.
admin.site.register(Answer)
admin.site.register(Attempt)
admin.site.register(Choice)
admin.site.register(Course)
admin.site.register(File)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(Section)
