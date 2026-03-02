from django.contrib import admin

from .models import Coach, Athlete, TrainingDay, TrainingPlan

admin.site.register(Coach)
admin.site.register(Athlete)
admin.site.register(TrainingDay)
admin.site.register(TrainingPlan)