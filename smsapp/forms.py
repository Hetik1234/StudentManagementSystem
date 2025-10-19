from django import forms
from .models import StudentModel

class StudentForm(forms.ModelForm):
    class Meta:
        model = StudentModel
        fields = "__all__"
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Student ID'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter Student Name'
            }),
            'marks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Marks (0-100)',
                'min': '0',
                'max': '100',
                'step': '1'
            }),
        }
    
    def clean_marks(self):
        marks = self.cleaned_data['marks']
        if marks < 0:
            raise forms.ValidationError("Marks cannot be less than 0%")
        if marks > 100:
            raise forms.ValidationError("Marks cannot exceed 100%")
        return marks
    
    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if not student_id:
            raise forms.ValidationError("Student ID is required")
        
        # Check for duplicate (for create operation)
        if not self.instance.pk and StudentModel.objects.filter(student_id=student_id).exists():
            raise forms.ValidationError("Student ID already exists!")
        
        return student_id