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


def hodd_home(request):
    hodd = get_object_or_404(Hodd, admin=request.user)

    # Get the faculty associated with the dean
    department = hodd.department

    department_course_list = Course.objects.filter(department=department)
    department_staff_list = Staff.objects.filter(subject__course__department=department)
    department_student_list = Student.objects.filter(course__department=department)
    department_subjects_list = Subject.objects.filter(course__department=department)
    department_attendance_list = Attendance.objects.filter(student__course__department=department)

    total_department_students = department_student_list.count()
    total_department_subjects = department_subjects_list.count()
    total_department_staff = department_staff_list.count()
    total_department_attendance = department_attendance_list.count()
    total_department_course = department_course_list.count()

    context = {
        'page_title': f'Dean Panel - {hodd.admin.last_name} ({department.department_name})',
        'total_department_students': total_department_students,
        'total_department_subjects': total_department_subjects,
        'total_department_staff': total_department_staff,
        'total_department_attendance': total_department_attendance,
        'total_department_course': total_department_course,
        'department_course_list': department_course_list,
        'department_staff_list': department_staff_list,
        'department_student_list': department_student_list,
        'department_subjects_list': department_subjects_list,
        'department_attendance_list': department_attendance_list,
    }
    return render(request, 'dean_template/home_content.html', context)

def hodd_veiw_course(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    courses = Course.objects.filter(department=hodd.faculty,)
    context ={
        'courses': courses,
        'page_title': 'View Courses',
    }
    return render(request, 'hodd_template/hodd_veiw_courses.html', context)

def hodd_veiw_subject(request, course_id):
    hodd = get_object_or_404(Hodd, admin=request.user)
    subjects = Subject.objects.filter(course__department=hodd.faculty, course__id=course_id)
    context = {
        'subjects': subjects,
        'page_title': 'View Subjects',
    }
    return render(request, 'hodd_template/hodd_veiw_subjects.html', context)

def hodd_veiw_staff(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    staff_members = Staff.objects.filter(subject__course__department=hodd.faculty)
    context = {
        'staff_members': staff_members,
        'page_title': 'View Staff',
    }
    return render(request, 'hodd_template/hodd_veiw_staff.html', context)

def hodd_veiw_student(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    students = Student.objects.filter(course__department=hodd.faculty)
    context = {
        'students': students,
        'page_title': 'View Students',
    }
    return render(request, 'hodd_template/hodd_veiw_sudents.html', context)

def hodd_view_attendance(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    subjects = Subject.objects.all(student__course__department=hodd.department)
    sessions = Session.objects.all(student__course__department=hodd.department)
    context = {
        'subjects': subjects,
        'sessions': sessions,
        'page_title': 'View Attendance'
    }
    return render(request, 'hodd_template/hodd_veiw_attendence.html', context)

def get_hodd_attendance(request):
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

def hodd_veiw_notification(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    # Fetch notifications related to the dean's faculty
    # You need to modify the query based on your notification model and relationships
    notifications = NotificationHodd.objects.filter(hodd=hodd)
    context = {
        'notifications': notifications,
        'page_title': 'View Notifications',
    }
    return render(request, 'hodd_template/hodd_veiw_notification.html', context)

def hodd_view_profile(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    form = HoddEditForm(request.POST or None, request.FILES or None,instance=hodd)
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
                admin = hodd.admin
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
                hodd.save()
                messages.success(request, "Profile Updated!")
                return redirect(reverse('hodd_view_profile'))
            else:
                messages.error(request, "Invalid Data Provided")
                return render(request, "hodd_template/hodd_view_profile.html", context)
        except Exception as e:
            messages.error(
                request, "Error Occured While Updating Profile " + str(e))
            return render(request, "hodd_template/hodd_view_profile.html", context)

    return render(request, "hodd_template/hodd_view_profile.html", context)

@csrf_exempt
def hodd_fcmtoken(request):
    token = request.POST.get('token')
    try:
        hodd_user = get_object_or_404(CustomUser, id=request.user.id)
        hodd_user.fcm_token = token
        hodd_user.save()
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")

def hodd_apply_leave(request):
    form = LeaveReportHoddForm(request.POST or None)
    hodd = get_object_or_404(Hodd, admin_id=request.user.id)
    context = {
        'form': form,
        'leave_history': LeaveReportStaff.objects.filter(hodd=hodd),
        'page_title': 'Apply for Leave'
    }
    if request.method == 'POST':
        if form.is_valid():
            try:
                obj = form.save(commit=False)
                obj.hodd = hodd
                obj.save()
                messages.success(
                    request, "Application for leave has been submitted for review")
                return redirect(reverse('hodd_apply_leave'))
            except Exception:
                messages.error(request, "Could not apply!")
        else:
            messages.error(request, "Form has errors!")
    return render(request, 'hodd_template/hodd_appy_leave.html', context)
def hodd_update_student_results(request):
    
    context ={
        
    }
    return render(request, 'hodd_template/hodd_update_results.html', context)

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

def hodd_view_notification(request):
    hodd = get_object_or_404(Staff, admin=request.user)
    notifications = NotificationHodd.objects.filter(hodd=hodd)
    context = {
        'notifications': notifications,
        'page_title': "View Notifications"
    }
    return render(request, 'hodd_template/hodd_view_notification.html', context)

@csrf_exempt
def staff_feedback_message(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStaff.objects.all(subject__course__department__faculty=hodd.faculty)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Staff Feedback Messages'
        }
        return render(request, 'hodd_template/staff_feedback_template.html', context)
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
    
    

def hodd_notify_staff(request):
    staff = CustomUser.objects.filter(user_type=4)
    context = {
        'page_title': "Send Notifications To Staff",
        'allStaff': staff
    }
    return render(request, 'hodd_template/staff_notification.html', context)

def send_staff_notification(request):
    id = request.POST.get('id')
    message = request.POST.get('message')
    staff = get_object_or_404(Staff, admin= request.user)
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
def view_student_leave(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    if request.method != 'POST':
        allLeave = LeaveReportStudent.objects.all(course__department__faculty=hodd.faculty)
        context = {
            'allLeave': allLeave,
            'page_title': 'Leave Applications From Students'
        }
        return render(request, 'hodd_template/student_leave_view.html', context)
    else:
        id = request.POST.get('id')
        status = request.POST.get('status')
        if (status == '1'):
            status = 1
        else:
            status = -1
        try:
            leave = get_object_or_404(LeaveReportStudent, id=id)
            leave.status = status
            leave.save()
            return HttpResponse(True)
        except Exception as e:
            return False

@csrf_exempt
def student_feedback_message(request):
    hodd = get_object_or_404(Hodd, admin=request.user)
    if request.method != 'POST':
        feedbacks = FeedbackStudent.objects.all(course__department__faculty=hodd.faculty)
        context = {
            'feedbacks': feedbacks,
            'page_title': 'Student Feedback Messages'
        }
        return render(request, 'hodd_template/student_feedback.html', context)
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

    

def hodd_notify_student(request):
    student = CustomUser.objects.filter(user_type=5)
    context = {
        'page_title': "Send Notifications To Students",
        'students': student
    }
    return render(request, 'hodd_template/student_notification.html', context)

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
