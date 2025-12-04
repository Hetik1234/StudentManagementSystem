from django.test import TestCase
from smsapp.models import StudentModel

class TestStudentModel(TestCase):

    def test_grade_h1(self):
        student = StudentModel(student_id="S1", name="Test Student", marks=85)
        self.assertEqual(student.grade, "H1")

    def test_grade_h2_1(self):
        student = StudentModel(student_id="S2", name="Test Student", marks=65)
        self.assertEqual(student.grade, "H2.1")

    def test_grade_h2_2(self):
        student = StudentModel(student_id="S3", name="Test Student", marks=55)
        self.assertEqual(student.grade, "H2.2")

    def test_grade_pass(self):
        student = StudentModel(student_id="S4", name="Test Student", marks=45)
        self.assertEqual(student.grade, "Pass")

    def test_grade_fail(self):
        student = StudentModel(student_id="S5", name="Test Student", marks=25)
        self.assertEqual(student.grade, "Fail")
