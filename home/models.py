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

class TrainingPlan(models.Model):
    athlete = models.ForeignKey(Athlete, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.athlete.user.username + ": " + str(self.start_date) + " - " + str(self.end_date)

class TrainingDay(models.Model):
    plan = models.ForeignKey(TrainingPlan, on_delete=models.CASCADE)
    date = models.DateField()
    distance = models.FloatField()

    def __str__(self):
        return self.plan.athlete.user.username + " day"