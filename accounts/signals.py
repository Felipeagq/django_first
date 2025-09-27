from django.db.models.signals import post_migrate
from django.dispatch import receiver
from .models import Role

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    if sender.name == "accounts":
        for role in ["admin", "student", "teacher","sales"]:
            Role.objects.get_or_create(name=role)