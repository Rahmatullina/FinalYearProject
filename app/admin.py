from .models import Student, Educator, Subject, Group, Timetable, Attendance
from django.contrib import admin

admin.site.register(Student)
admin.site.register(Educator)
admin.site.register(Subject)
admin.site.register(Group)
admin.site.register(Timetable)
admin.site.register(Attendance)