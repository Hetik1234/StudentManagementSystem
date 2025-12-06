"""Models for the StudentMS application."""

from django.db import models


class StudentModel(models.Model):
    """Model representing a student with marks and a computed grade."""
    student_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=30)
    marks = models.IntegerField()

    @property
    def grade(self):
        """Calculate grade based on marks (H1, H2.1, H2.2, Pass, Fail)."""
        marks = float(self.marks)
        if marks >= 70:
            return "H1"
        if marks >= 60:
            return "H2.1"
        if marks >= 50:
            return "H2.2"
        if marks >= 40:
            return "Pass"
        return "Fail"

    def __str__(self):
        """Human-readable representation of the student."""
        return f"{self.student_id} - {self.name}"
