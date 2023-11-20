from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
# Register your models here.


class UserModel(UserAdmin):
    ordering = ('email',)


admin.site.register(CustomUser, UserModel)
admin.site.register(Dean)
admin.site.register(Hodd)
admin.site.register(Staff)
admin.site.register(Student)
admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Test_Attendance)
admin.site.register(Test_Student)
admin.site.register(Test_Student_Attendance)
admin.site.register(Test_Student_Image)
