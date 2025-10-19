from django.db import models
class StudentModel(models.Model):
	student_id = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=30)
	marks = models.IntegerField()

	@property
	def grade(self):
		"""Calculate Master's degree grade based on marks"""
		marks = float(self.marks)
		if marks >= 70:
			return 'H1'
		elif marks >= 60:
			return 'H2.1'
		elif marks >= 50:
			return 'H2.2'
		elif marks >= 40:
			return 'Pass'
		else:
			return 'Fail'
    
	def __str__(self):
		return f"{self.student_id} - {self.name}"