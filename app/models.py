from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, default='default')
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    degree = [('UG','undergraduate'),('G','graduate')]
    entry_year = models.IntegerField()
    graduate_year = models.IntegerField()
    study_form = [('FT','full-time'),('PT','part-time')]

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " "+ self.group.name


class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, default='default')
    departament = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.middle_name +  " " +  self.position + " " + self.departament


class Subject(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class EducatorAndSubject(models.Model):
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    educator = models.ForeignKey('Educator', on_delete=models.CASCADE)
    group = models.ForeignKey('Group', on_delete=models.CASCADE)


class Timetable(models.Model):
    group = models.ForeignKey('Group', on_delete=models.CASCADE)
    date = models.DateTimeField()
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    educator = models.ForeignKey('Educator', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.date) + " " + self.group.name + " "  + self.subject.name


class Attendance(models.Model):
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    attended = models.BooleanField()

    def __str__(self):
        return str(self.timetable.date) + " " + str(self.student) + " "  + self.timetable.subject.name