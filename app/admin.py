from .models import Student, Educator, Timetable, Attendance
from django.contrib import admin

class StudentAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Student, StudentAdmin)

# admin.site.register(Student)
admin.site.register(Educator)
# admin.site.register(Subject)
# admin.site.register(Group)
admin.site.register(Timetable)
admin.site.register(Attendance)