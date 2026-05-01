from django import forms
from .models import Timetable, Lesson, BellSchedule, Period


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = ['name', 'bell_schedule', 'academic_year', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Term 1 2025-26',
            }),
            'bell_schedule': forms.Select(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 2025-26',
            }),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date':   forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['bell_schedule'].queryset = BellSchedule.objects.filter(owner=user)
        else:
            self.fields['bell_schedule'].queryset = BellSchedule.objects.none()
        self.fields['bell_schedule'].required = False
        self.fields['academic_year'].required = False
        self.fields['start_date'].required    = False
        self.fields['end_date'].required      = False


class BellScheduleForm(forms.ModelForm):
    class Meta:
        model = BellSchedule
        fields = ['name', 'working_days', 'is_default']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Standard Bell Schedule'}),
            'working_days': forms.CheckboxSelectMultiple(choices=[
                (0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'),
                (3, 'Thursday'), (4, 'Friday'), (5, 'Saturday'),
            ]),
            'is_default': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PeriodForm(forms.ModelForm):
    class Meta:
        model = Period
        fields = ['name', 'period_number', 'start_time', 'end_time', 'period_type']
        widgets = {
            'name':          forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Period 1'}),
            'period_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'start_time':    forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time':      forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'period_type':   forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get('start_time')
        end   = cleaned.get('end_time')
        if start and end and end <= start:
            raise forms.ValidationError('End time must be after start time.')
        return cleaned


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'faculty', 'division', 'room', 'periods_per_week']
        widgets = {
            'subject':         forms.Select(attrs={'class': 'form-control'}),
            'faculty':         forms.Select(attrs={'class': 'form-control'}),
            'division':        forms.Select(attrs={'class': 'form-control'}),
            'room':            forms.Select(attrs={'class': 'form-control'}),
            'periods_per_week': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 30}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        from resources.models import Subject, Division, Room
        from faculty.models import Faculty
        if user:
            self.fields['subject'].queryset  = Subject.objects.filter(owner=user)
            self.fields['faculty'].queryset  = Faculty.objects.filter(owner=user, status='active')
            self.fields['division'].queryset = Division.objects.all().select_related('grade')
            self.fields['room'].queryset     = Room.objects.filter(owner=user)
        else:
            self.fields['subject'].queryset  = Subject.objects.none()
            self.fields['faculty'].queryset  = Faculty.objects.none()
            self.fields['division'].queryset = Division.objects.none()
            self.fields['room'].queryset     = Room.objects.none()
        self.fields['faculty'].required = False
        self.fields['room'].required    = False