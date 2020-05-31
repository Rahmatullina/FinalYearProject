from django.contrib.auth.models import User
from django.db import models

# class Group(models.Model):
#     name = models.CharField(max_length=10, unique=True)
#
#     def __str__(self):
#         return self.name


class Student(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, default='default')
    group = models.CharField(max_length=100)
    degree = models.CharField(
        max_length=20,
        choices=[('UG','Студент Бакалавриата'),('G','Магистрант')],
        default='UG',
    )
    entry_year = models.IntegerField()
    graduate_year = models.IntegerField()
    study_form = models.CharField(
        max_length=20,
        choices=[('FT','Очная форма обучения'),('PT','Заочная форма обучения')],
        default='FT',
    )

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.group


class Educator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=100, default='default')
    departament = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name + " " + self.middle_name +  " " +  self.position + " " + self.departament


class Timetable(models.Model):
    id = models.AutoField(primary_key=True)
    group = models.CharField(max_length=100)
    start = models.CharField(default='2020-03-02T09:30:00', max_length=25, blank=True)
    end = models.CharField(default='2020-03-03T09:30:00', max_length=25, blank=True)
    subject = models.CharField(max_length=500)
    educator = models.ForeignKey('Educator', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.start) + " " + self.group + " " + self.subject


class Attendance(models.Model):
    timetable = models.ForeignKey('Timetable', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    attended = models.BooleanField()
    emotion = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return str(self.timetable.start) + " " + str(self.student) + " "  + self.timetable.subject