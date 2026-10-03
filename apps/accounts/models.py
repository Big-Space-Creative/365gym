from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modelo de usuário customizado do 365-Gym.

    Herda todos os campos do AbstractUser (username, email, password, etc.).
    O campo `role` define o papel do usuário no sistema.
    """

    class Role(models.TextChoices):
        ALUNO = "aluno", "Aluno"
        PROFESSOR = "professor", "Professor"
        ADMINISTRADOR = "administrador", "Administrador"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.ALUNO,
        verbose_name="Papel",
    )

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
