from django.forms import ModelForm, DateInput, ValidationError
from django.utils import timezone

from .models import TrainingPlan, Athlete, TrainingDay

class TrainingPlanForm(ModelForm):
    class Meta:
        model = TrainingPlan 
        fields = ["athlete", "start_date", "end_date"]
        widgets = {
            "start_date": DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"}, 
            ),
            "end_date": DateInput(
                format="%Y-%m-%d",
                attrs={"type": "date"},
            )
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super(TrainingPlanForm, self).__init__(*args, **kwargs)

        if user:
            self.fields["athlete"].queryset = Athlete.objects.filter(coach__user=user)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("End date must be after start date.")
        return cleaned_data

class TrainingDayForm(ModelForm):
    class Meta:
        model = TrainingDay
        fields = ['distance']