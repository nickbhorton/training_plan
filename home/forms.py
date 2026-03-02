from django.forms import Form, DateField, DateInput, ValidationError

class TrainingPlanForm(Form):
    start_date = DateField(
        label = "Start Date",
        widget = DateInput(attrs={'type': 'date'}),
    )
    end_date = DateField(
        label = "End Date",
        widget = DateInput(attrs={'type': 'date'})
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("End date must be after start date.")
        return cleaned_data