from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Coach(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Athlete(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.username