from django import forms
from django.forms.widgets import DateInput, TextInput

from .models import *


class FormSettings(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSettings, self).__init__(*args, **kwargs)
        # Here make some changes such as:
        for field in self.visible_fields():
            field.field.widget.attrs['class'] = 'form-control'



class CustomUserForm(FormSettings):
    email = forms.EmailField(required=True)
    gender = forms.ChoiceField(choices=[('M', 'Male'), ('F', 'Female')])
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    address = forms.CharField(widget=forms.Textarea)
    password = forms.CharField(widget=forms.PasswordInput)
    widget = {
        'password': forms.PasswordInput(),
    }
    profile_pic = forms.ImageField()

    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)

        if kwargs.get('instance'):
            instance = kwargs.get('instance').admin.__dict__
            self.fields['password'].required = False
            for field in CustomUserForm.Meta.fields:
                self.fields[field].initial = instance.get(field)
            if self.instance.pk is not None:
                self.fields['password'].widget.attrs['placeholder'] = "Fill this only if you wish to update password"

    def clean_email(self, *args, **kwargs):
        formEmail = self.cleaned_data['email'].lower()
        if self.instance.pk is None:  # Insert
            if CustomUser.objects.filter(email=formEmail).exists():
                raise forms.ValidationError(
                    "The given email is already registered")
        else:  # Update
            dbEmail = self.Meta.model.objects.get(
                id=self.instance.pk).admin.email.lower()
            if dbEmail != formEmail:  # There has been changes
                if CustomUser.objects.filter(email=formEmail).exists():
                    raise forms.ValidationError("The given email is already registered")

        return formEmail

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'gender',  'password','profile_pic', 'address' ]


class AdminForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(AdminForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Admin
        fields = CustomUserForm.Meta.fields

class DeanForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(DeanForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Dean
        fields = CustomUserForm.Meta.fields + \
            ['faculty']

class HoddForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HoddForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Hodd
        fields = CustomUserForm.Meta.fields + \
            ['department']            


class StaffForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields + \
            ['course' ]
class StudentForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields + \
            ['course', 'session']
            

class FacultyForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name']
        model = Faculty
        
class DepartmentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(DepartmentForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name','faculty']
        model = Department        

class CourseForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)

    class Meta:
        fields = ['name', 'department']
        model = Course


class SubjectForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Subject
        fields = ['name', 'staff', 'course']


class SessionForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Session
        fields = '__all__'
        widgets = {
            'start_year': DateInput(attrs={'type': 'date'}),
            'end_year': DateInput(attrs={'type': 'date'}),
        }

class LeaveReportDeanForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportDeanForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportDean
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackDeanForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackDeanForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackDean
        fields = ['feedback']

class LeaveReportHoddForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportHoddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportHodd
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackHoddForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackHoddForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackHodd
        fields = ['feedback']

class LeaveReportStaffForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStaff
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStaffForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStaffForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStaff
        fields = ['feedback']


class LeaveReportStudentForm(FormSettings):
    def __init__(self, *args, **kwargs):
        super(LeaveReportStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = LeaveReportStudent
        fields = ['date', 'message']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
        }


class FeedbackStudentForm(FormSettings):

    def __init__(self, *args, **kwargs):
        super(FeedbackStudentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FeedbackStudent
        fields = ['feedback']


class StudentEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StudentEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Student
        fields = CustomUserForm.Meta.fields 


class StaffEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(StaffEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Staff
        fields = CustomUserForm.Meta.fields

class HoddEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(HoddEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Hodd
        fields = CustomUserForm.Meta.fields

class DeanEditForm(CustomUserForm):
    def __init__(self, *args, **kwargs):
        super(DeanEditForm, self).__init__(*args, **kwargs)

    class Meta(CustomUserForm.Meta):
        model = Dean
        fields = CustomUserForm.Meta.fields



class EditResultForm(FormSettings):
    session_list = Session.objects.all()
    session_year = forms.ModelChoiceField(
        label="Session Year", queryset=session_list, required=True)

    def __init__(self, *args, **kwargs):
        super(EditResultForm, self).__init__(*args, **kwargs)

    class Meta:
        model = StudentResult
        fields = ['session_year', 'subject', 'student', 'test', 'exam']
#class AttendanceForm(forms.Form):
#    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), empty_label="Select Subject")
#    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label="Select Program")
#    attendance_file = forms.FileField(label='Upload Attendance Video or Group Photo', required=True)


class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['session', 'subject', 'date']

    def __init__(self, *args, **kwargs):
        super(AttendanceForm, self).__init__(*args, **kwargs)
        self.fields['session'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['date'].widget.attrs.update({'class': 'form-control', 'type': 'date'})
        #self.fields['file'].widget.attrs.update({'class': 'form-control', 'accept': '.mp4, .jpg, .jpeg, .png', 'required': 'required'})
        
class StudentFaceImageForm(forms.ModelForm):
    class Meta:
        model = StudentFaceImage
        fields = ['face_image']


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True   
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result     
    

        
class UploadStudentImagesForm(forms.Form):
    student = forms.ModelChoiceField(queryset=Student.objects.all(), required=False)
    files = MultipleFileField()
    

    
    