from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse
from django.shortcuts import redirect


class LoginCheckMiddleWare(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        user = request.user # Who is the current user ?
        
        # Define an array of module names for each user type
        admin_modules = ['main_app.student_views', 'main_app.staff_views', 'main_app.dean_views', 'main_app.hodd_views']
        dean_modules = ['main_app.student_views', 'main_app.hod_views', 'main_app.staff_views', 'main_app.hodd_views']
        hodd_modules = ['main_app.student_views', 'main_app.hod_views', 'main_app.dean_views', 'main_app.saff_views']
        staff_modules = ['main_app.student_views', 'main_app.hod_views', 'main_app.dean_views', 'main_app.hodd_views']
        student_modules = ['main_app.hod_views', 'main_app.staff_views','main_app.dean_views','main_app.hodd_views']
        
        if user.is_authenticated:
            if user.user_type == '1': # Is it the Admin
                if modulename in admin_modules:
                    return redirect(reverse('admin_home'))
            elif user.user_type == '2': #  Dean :-/ ?
                if modulename in dean_modules:
                    return redirect(reverse('dean_home'))
            elif user.user_type == '3': # hodd ?
                if modulename in hodd_modules:
                    return redirect(reverse('hodd_home'))
            elif user.user_type == '4': #  staff :-/ ?
                if modulename in staff_modules:
                    return redirect(reverse('staff_home'))
            elif user.user_type == '5': # ... or Student ?
                if modulename in student_modules:
                    return redirect(reverse('student_home'))
            else: # None of the aforementioned ? Please take the user to login page
                return redirect(reverse('login_page'))
        else:
            if request.path == reverse('login_page') or modulename == 'django.contrib.auth.views' or request.path == reverse('user_login'): # If the path is login or has anything to do with authentication, pass
                pass
            else:
                return redirect(reverse('login_page'))
