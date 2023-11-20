"""college_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from main_app.EditResultView import EditResultView

from . import dean_views, hod_views, hodd_views, staff_views, student_views, views


urlpatterns = [
     
    path("", views.login_page, name='login_page'),
    path("get_attendance", views.get_attendance, name='get_attendance'),
    path("firebase-messaging-sw.js", views.showFirebaseJS, name='showFirebaseJS'),
    path("doLogin/", views.doLogin, name='user_login'),
    path("logout_user/", views.logout_user, name='user_logout'),
    path("admin/home/", hod_views.admin_home, name='admin_home'),
    path("course/add", hod_views.add_course, name='add_course'),
    path("department/add", hod_views.add_department, name = 'add_department'),
    path("faculty/add", hod_views.add_faculty, name= 'add_faculty'),
    path("send_student_notification/", hod_views.send_student_notification,
         name='send_student_notification'),
    path("send_staff_notification/", hod_views.send_staff_notification,
         name='send_staff_notification'),
    path("send_hodd_notification/", hod_views.send_hodd_notification,
         name='send_hodd_notification'),
    path("send_dean_notification/", hod_views.send_dean_notification,
         name='send_dean_notification'),
    path("add_session/", hod_views.add_session, name='add_session'),
    path("admin_notify_student", hod_views.admin_notify_student,
         name='admin_notify_student'),
    path("admin_notify_staff", hod_views.admin_notify_staff,
         name='admin_notify_staff'),
    path("admin_notify_hodd", hod_views.admin_notify_hodd,
         name='admin_notify_hodd'),
    path("admin_notify_dean", hod_views.admin_notify_dean,
         name='admin_notify_dean'),
    path("admin_view_profile", hod_views.admin_view_profile,
         name='admin_view_profile'),
    path("check_email_availability", hod_views.check_email_availability,
         name="check_email_availability"),
    path("session/manage/", hod_views.manage_session, name='manage_session'),
    path("session/edit/<int:session_id>",
         hod_views.edit_session, name='edit_session'),
    path("student/view/feedback/", hod_views.student_feedback_message,
         name="student_feedback_message",),
    path("staff/view/feedback/", hod_views.staff_feedback_message,
         name="staff_feedback_message",),
    path("hodd/view/feedback/", hod_views.hodd_feedback_message,
         name="hodd_feedback_message",),
    path("dean/view/feedback/", hod_views.dean_feedback_message,
         name="dean_feedback_message",),
    path("student/view/leave/", hod_views.view_student_leave,
         name="view_student_leave",),
    path("hodd/view/leave/", hod_views.view_hodd_leave,
         name="view_staff_leave",),
    path("dean/view/leave/", hod_views.view_dean_leave,
         name="view_student_leave",),
    path("staff/view/leave/", hod_views.view_staff_leave,
         name="view_staff_leave",),
    path("attendance/view/", hod_views.admin_view_attendance,
         name="admin_view_attendance",),
    path("attendance/fetch/", hod_views.get_admin_attendance,
         name='get_admin_attendance'),
    path("student/add/", hod_views.add_student, name='add_student'),
    path("staff/add", hod_views.add_staff, name='add_staff'),
    path("hodd/add/", hod_views.add_hodd, name='add_hodd'),
    path("dean/add/", hod_views.add_dean, name='add_dean'),
    path("subject/add/", hod_views.add_subject, name='add_subject'),
    path("staff/manage/", hod_views.manage_staff, name='manage_staff'),
    path("hodd/manage/", hod_views.manage_hodd, name='manage_hodd'),
    path("dean/manage/", hod_views.manage_dean, name='manage_dean'),
    path("student/manage/", hod_views.manage_student, name='manage_student'),
    path("faculty/manage/", hod_views.manage_faculty, name='manage_faculty'),
    path("department/manage/", hod_views.manage_department, name = 'manage_department'),
    path("course/manage/", hod_views.manage_course, name='manage_course'),
    path("subject/manage/", hod_views.manage_subject, name='manage_subject'),
    path("edit/<int:dean_id>", hod_views.edit_dean, name='edit_dean'),
    path("hodd/edit/<int:hodd_id>", hod_views.edit_hodd, name='edit_hodd'),
    path("staff/edit/<int:staff_id>", hod_views.edit_staff, name='edit_staff'),
    path("dean/delete/<int:dean_id>",
         hod_views.delete_dean, name='delete_dean'),
    path("hodd/delete/<int:hodd_id>",
         hod_views.delete_hodd, name='delete_hodd'),
    path("staff/delete/<int:staff_id>",
         hod_views.delete_staff, name='delete_staff'),

    path("faculty/delete/<int:faculty_id>",
         hod_views.delete_faculty, name = 'delete_faculty'),
    path("course/delete/<int:course_id>",
         hod_views.delete_course, name='delete_course'),
    
    path("department/delete/<int:department_id>",
         hod_views.delete_department, name = 'delete_department'),

    path("subject/delete/<int:subject_id>",
         hod_views.delete_subject, name='delete_subject'),

    path("session/delete/<int:session_id>",
         hod_views.delete_session, name='delete_session'),

    path("student/delete/<int:student_id>",
         hod_views.delete_student, name='delete_student'),
    path("student/edit/<int:student_id>",
         hod_views.edit_student, name='edit_student'),
    path("faculty/edit/<int:faculty_id>",
         hod_views.edit_faculty, name = 'edit_faculty'),
    path("department/edit/<int:department_id>",
         hod_views.edit_department, name = 'edit_department'),
    path("course/edit/<int:course_id>",
         hod_views.edit_course, name='edit_course'),
    path("subject/edit/<int:subject_id>",
         hod_views.edit_subject, name='edit_subject'),
    
    
    #Dean
     path("dean/home/", dean_views.dean_home, name='dean_home'),
     path("send_student_notification/", dean_views.send_student_notification,
         name='send_student_notification'),
     path("send_staff_notification/", dean_views.send_staff_notification,
         name='send_staff_notification'),
     path("send_hodd_notification/", dean_views.send_hodd_notification,
         name='send_hodd_notification'),
     path("dean_notify_student", dean_views.dean_notify_student,
         name='dean_notify_student'),
     path("dean_notify_staff", dean_views.dean_notify_staff,
         name='dean_notify_staff'),
     path("dean_notify_hodd", dean_views.dean_notify_hodd,
         name='dean_notify_hodd'),
     path("dean_view_profile", dean_views.dean_view_profile,
         name='dean_view_profile'),
     path("check_email_availability", dean_views.check_email_availability,
         name="check_email_availability"),
     path("hodd/view/feedback/", dean_views.hodd_feedback_message,
         name="hodd_feedback_message",),
     path("staff/view/feedback/", dean_views.staff_feedback_message,
         name="staff_feedback_message",),
     path("student/view/feedback/", dean_views.student_feedback_message,
         name="student_feedback_message",),
     path("staff/view/leave/", dean_views.view_staff_leave,
         name="view_staff_leave",),
     path("attendance/view/", dean_views.dean_view_attendance,
         name="dean_view_attendance",),
    path("attendance/fetch/", dean_views.get_dean_attendance,
         name='get_dean_attendance'),
    
     
    #Hodd
     path("hodd/home/", hodd_views.hodd_home, name='hodd_home'),
     path("send_student_notification/", hodd_views.send_student_notification,
         name='send_student_notification'),
     path("send_staff_notification/", hodd_views.send_staff_notification,
         name='send_staff_notification'),
     path("hodd_notify_staff", hodd_views.hodd_notify_staff,
          name='hodd_notify_staff'),
     path("hodd_notify_student", hodd_views.hodd_notify_student,
          name='hodd_notify_student'),
     path("hodd_view_profile", hodd_views.hodd_view_profile,
         name='hodd_view_profile'),
    path("check_email_availability", hodd_views.check_email_availability,
         name="check_email_availability"),
    path("staff/view/feedback/", hodd_views.staff_feedback_message,
         name="staff_feedback_message",),
     path("student/view/feedback/", hodd_views.student_feedback_message,
         name="student_feedback_message",),
     path("staff/view/leave/", hodd_views.view_student_leave,
         name="view_student_leave",),
     path("attendance/fetch/", hodd_views.get_hodd_attendance,
         name='get_hodd_attendance'),
     path("attendance/view/", hodd_views.hodd_view_attendance,
         name="hodd_view_attendance",),
    path("attendance/fetch/", hodd_views.get_hodd_attendance,
         name='get_hodd_attendance'),


    # Staff
    path("staff/home/", staff_views.staff_home, name='staff_home'),
    path("staff/apply/leave/", staff_views.staff_apply_leave,
         name='staff_apply_leave'),
    path("staff/feedback/", staff_views.staff_feedback, name='staff_feedback'),
    path("staff/view/profile/", staff_views.staff_view_profile,
         name='staff_view_profile'),
    path("staff/attendance/take/", staff_views.staff_take_attendance,
         name='staff_take_attendance'),
    path("staff/attendance/update/", staff_views.staff_update_attendance,
         name='staff_update_attendance'),
    path("staff/get_students/", staff_views.get_students, name='get_students'),
    path("staff/attendance/fetch/", staff_views.get_student_attendance,
         name='get_student_attendance'),
    path("staff/attendance/save/",
         staff_views.save_attendance, name='save_attendance'),
    path("staff/attendance/update/",
         staff_views.update_attendance, name='update_attendance'),
    path("staff/fcmtoken/", staff_views.staff_fcmtoken, name='staff_fcmtoken'),
    path("staff/view/notification/", staff_views.staff_view_notification,
         name="staff_view_notification"),
    path("staff/result/add/", staff_views.staff_add_result, name='staff_add_result'),
    path("staff/result/edit/", EditResultView.as_view(),
         name='edit_student_result'),
    path('staff/result/fetch/', staff_views.fetch_student_result,
         name='fetch_student_result'),
    #path('upload/attendance/', staff_views.upload_attendance, name='upload_attendance'),
    
   




    # Student
    path("student/home/", student_views.student_home, name='student_home'),
    path("student/view/attendance/", student_views.student_view_attendance,
         name='student_view_attendance'),
    path("student/apply/leave/", student_views.student_apply_leave,
         name='student_apply_leave'),
    path("student/feedback/", student_views.student_feedback,
         name='student_feedback'),
    path("student/view/profile/", student_views.student_view_profile,
         name='student_view_profile'),
    path("student/fcmtoken/", student_views.student_fcmtoken,
         name='student_fcmtoken'),
    path("student/view/notification/", student_views.student_view_notification,
         name="student_view_notification"),
    path('student/view/result/', student_views.student_view_result,
         name='student_view_result'),
    path('student/upload/image/', student_views.upload_student_images,
         name='upload_student_images'),
    


    path('collect-attendance', staff_views.collect_attendance, name='collect'),
    path('add-student-images', staff_views.add_student_images, name='add_images'),
    path('make-attendance', staff_views.make_attendance, name='make_attendance'),
    path('try-attendance', staff_views.anylse_all_faces, name='anylse_all_faces'),

]
