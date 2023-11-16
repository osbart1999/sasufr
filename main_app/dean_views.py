import json
import requests
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import (HttpResponse, HttpResponseRedirect,
                              get_object_or_404, redirect, render)
from django.templatetags.static import static
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView

from .forms import *
from .models import *


def dean_home(request):
    dean = get_object_or_404(Dean, admin=request.user)

    # Get the faculty associated with the dean
    faculty = dean.faculty

    faculty_department_list = Department.objects.filter(faculty=faculty)
    faculty_course_list = Course.objects.filter(department__faculty=faculty)
    faculty_staff_list = Staff.objects.filter(subject__course__department__faculty=faculty)
    faculty_student_list = Student.objects.filter(course__department__faculty=faculty)
    faculty_subjects_list = Subject.objects.filter(course__department__faculty=faculty)
    faculty_attendance_list = Attendance.objects.filter(student__course__department__faculty=faculty)

    total_faculty_students = faculty_student_list.count()
    total_faculty_subjects = faculty_subjects_list.count()
    total_faculty_department = faculty_department_list.count()
    total_faculty_staff = faculty_staff_list.count()
    total_faculty_attendance = faculty_attendance_list.count()
    total_faculty_course = faculty_course_list.count()

    context = {
        'page_title': f'Dean Panel - {dean.admin.last_name} ({faculty.faculty_name})',
        'total_faculty_students': total_faculty_students,
        'total_faculty_subjects': total_faculty_subjects,
        'total_faculty_department': total_faculty_department,
        'total_faculty_staff': total_faculty_staff,
        'total_faculty_attendance': total_faculty_attendance,
        'total_faculty_course': total_faculty_course,
        'faculty_department_list': faculty_department_list,
        'faculty_course_list': faculty_course_list,
        'faculty_staff_list': faculty_staff_list,
        'faculty_student_list': faculty_student_list,
        'faculty_subjects_list': faculty_subjects_list,
        'faculty_attendance_list': faculty_attendance_list,
    }
    return render(request, 'dean_template/home_content.html', context)
@ csrf_exempt
def dean_veiw_department(request):
    dean = get_object_or_404(Dean, admin=request.user)
    department = Department.objects.filter(faculty=dean.faculty)
    context = {
        'department': department,
        'page_title': 'View Departments'
    
    }
    return render(request, 'dean_template/dean_veiw_department.html', context)

def dean_veiw_course(request, department_id):
    dean = get_object_or_404(Dean, admin=request.user)
    courses = Course.objects.filter(department__faculty=dean.faculty, department__id=department_id)
    context ={
        'courses': courses,
        'page_title': 'View Courses',
    }
    return render(request, 'dean_template/dean_veiw_courses.html', context)

def dean_view_subject(request, course_id):
    dean = get_object_or_404(Dean, admin=request.user)
    subjects = Subject.objects.filter(course__department__faculty=dean.faculty, course__id=course_id)
    context = {
        'subjects': subjects,
        'page_title': 'View Subjects',
    }
    return render(request, 'dean_template/dean_view_subjects.html', context)

def dean_view_staff(request):
    dean = get_object_or_404(Dean, admin=request.user)
    staff_members = Staff.objects.filter(subject__course__department__faculty=dean.faculty)
    context = {
        'staff_members': staff_members,
        'page_title': 'View Staff',
    }
    return render(request, 'dean_template/dean_view_staff.html', context)

def dean_view_student(request):
    dean = get_object_or_404(Dean, admin=request.user)
    students = Student.objects.filter(course__department__faculty=dean.faculty)
    context = {
        'students': students,
        'page_title': 'View Students',
    }
    return render(request, 'dean_template/dean_view_students.html', context)


def dean_view_attendance(request):
    dean = get_object_or_404(Dean, admin=request.user)
    subjects = Subject.objects.all(student__course__department__faculty=dean.faculty)
    sessions = Session.objects.all(student__course__department__faculty=dean.faculty)
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }
    return render(request, 'dean_template/dean_view_students.html', context)

def get_dean_attendance(request):
    subject_id = request.POST.get('subject')
    session_id = request.POST.get('session')
    attendance_date_id = request.POST.get('attendance_date_id')
    try:
        subject = get_object_or_404(Subject, id=subject_id)
        session = get_object_or_404(Session, id=session_id)
        attendance = get_object_or_404(
            Attendance, id=attendance_date_id, session=session)
        attendance_reports = AttendanceReport.objects.filter(
            attendance=attendance)
        json_data = []
        for report in attendance_reports:
            data = {
                "status":  str(report.status),
                "name": str(report.student)
            }
            json_data.append(data)
        return JsonResponse(json.dumps(json_data), safe=False)
    except Exception as e:
        return None

def dean_view_profile(request):
    dean = get_object_or_404(Dean, admin=request.user)
    form = DeanEditForm(request.POST or None, request.FILES or None,instance=dean)
    context = {'form': form, 'page_title': 'View/Update Profile'}
    if request.method == 'POST':
        try:
            if form.is_valid():
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                password = form.cleaned_data.get('password') or None
                address = form.cleaned_data.get('address')
                gender = form.cleaned_data.get('gender')
                passport = request.FILES.get('profile_pic') or None
                admin = dean.admin
                if password != None:
                    admin.set_password(password)
                if passport != None:
                    fs = FileSystemStorage()
                    filename = fs.save(passport.name, passport)
                    passport_url = fs.url(filename)
                    admin.profile_pic = passport_url
                admin.first_name = first_name
                admin.last_name = last_name
                admin.address = address
                admin.gender = gender
                admin.save()
                dean.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('dean_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "staff_template/dean_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "dean_template/dean_view_profile.html", context)

    return render(request, "dean_template/dean_view_profile.html", context)

@csrf_exempt
def dean_fcmtoken(request):
    token = request.POST.get('token')
    try:
        dean_user = get_object_or_404(CustomUser, id=request.user.id)
        dean_user.fcm_token = token
        dean_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

def hodd_apply_leave(request):
    form = LeaveReportDeanForm(request.POST or None)
    dean = get_object_or_404(Hodd, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(hodd=dean),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.dean = dean
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('dean_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, 'dean_template/dean_appy_leave.html', context)
def dean_update_student_results(request):
    
    context ={
        
    }
    return render(request, 'dean_template/dean_update_results.html', context)

@csrf_exempt
def check_email_availability(request):
    email = request.POST.get("email")
    try:
        user = CustomUser.objects.filter(email=email).exists()
        if user:
            return HttpResponse(True)
        return HttpResponse(False)
    except Exception as e:
        return HttpResponse(False)
@csrf_exempt
def hodd_feedback_message(request):
    dean = get_object_or_404(Dean, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackHodd.objects.all(faculty=dean.faculty)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Hodd Feedback Messages'
        }
        return render(request, 'dean_template/hodd_feedback.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackHodd, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)
    

def dean_view_notification(request):
    dean = get_object_or_404(Dean, admin=request.user)
    # Fetch notifications related to the dean's faculty
    # You need to modify the query based on your notification model and relationships
    notifications = NotificationDean.objects.filter(dean=dean)
    context = {
        'notifications': notifications,
        'page_title': 'View Notifications',
    }
    return render(request, 'dean_template/dean_view_notification.html', context)

def dean_notify_hodd(request):
    hodd = CustomUser.objects.filter(user_type=3)
    context = {
        'page_title': "Send Notifications To Hodd",
        'allHodd': hodd
    }
    return render(request, 'dean_template/hodd_notification.html', context)

def send_hodd_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    hodd = get_object_or_404(Hodd, admin_id= id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Atendence System Using Face Recongniton",
                'body': message,
                'click_action': reverse('hodd_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': hodd.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationHodd(hodd=hodd, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
    
def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin_id= id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Management System",
                'body': message,
                'click_action': reverse('staff_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': staff.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStaff(staff=staff, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message(request):
    dean = get_object_or_404(Dean, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all(subject__course__department__faculty=dean.faculty)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'dean_template/staff_feedback.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStaff, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)
    

def dean_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=4)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, 'dean_template/staff_notification.html', context)
@csrf_exempt
def view_staff_leave(request):
    dean = get_object_or_404(Dean, admin=request.user)
    if request.method != 'POST':
        allLeave = LeaveReportStaff.objects.filter(subject__course__department__faculty=dean.faculty)
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Staff'
        }
        return render(request, 'dean_template/staff_leave_view.html', context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStaff, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False

@csrf_exempt
def student_feedback_message(request):
    dean = get_object_or_404(Dean, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all(course__department__faculty=dean.faculty)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'dean_template/student_feedback.html', context)
    else:
        feedback_id = request.POST.get('id')
        try:
            feedback = get_object_or_404(FeedbackStudent, id=feedback_id)
            reply = request.POST.get('reply')
            feedback.reply = reply
            feedback.save()
            return HttpResponse(True)
        except Exception as e:
            return HttpResponse(False)

    

def dean_notify_student(request):
    student = CustomUser.objects.filter(user_type=5)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, 'dean_templatestudent_notification/.html', context)

@csrf_exempt
def send_student_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    student = get_object_or_404(Student, admin_id= id)
    try:
        url = "https://fcm.googleapis.com/fcm/send"
        body = {
            'notification': {
                'title': "Student Attendence System Using Face Recognition",
                'body': message,
                'click_action': reverse('student_view_notification'),
                'icon': static('dist/img/AdminLTELogo.png')
            },
            'to': student.admin.fcm_token
        }
        headers = {'Authorization':
                   'key=AAAA3Bm8j_M:APA91bElZlOLetwV696SoEtgzpJr2qbxBfxVBfDWFiopBWzfCfzQp2nRyC7_A2mlukZEHV4g1AmyC6P_HonvSkY2YyliKt5tT3fe_1lrKod2Daigzhb2xnYQMxUWjCAIQcUexAMPZePB',
                   'Content-Type': 'application/json'}
        data = requests.post(url, data=json.dumps(body), headers=headers)
        notification = NotificationStudent(student=student, message=message)
        notification.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
