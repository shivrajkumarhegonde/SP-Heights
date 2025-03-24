from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import MaintenanceRequest, Event, Notice, Complaint, CustomUser
from .models import Document
from .models import Member
from datetime import date
class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'phone_number', 'flat_number', 'role', 'email', 'address']

    def clean_flat_number(self):
        flat_number = self.cleaned_data.get('flat_number')
        if Member.objects.filter(flat_number=flat_number).exists():
            raise forms.ValidationError("This flat number is already assigned to another member.")
        return flat_number
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'file']

User = get_user_model()

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    phone_number = forms.CharField(max_length=15, required=True)
    flat_number = forms.CharField(max_length=10, required=True)
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'flat_number', 'user_type', 'password1', 'password2')

class MaintenanceRequestForm(forms.ModelForm):
    class Meta:
        model = MaintenanceRequest
        fields = ['title', 'description']

class EventForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().strftime('%Y-%m-%d')  # Restricts past dates
            }
        )
    )

    class Meta:
        model = Event
        fields = ['name', 'date', 'description']

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ['title', 'description']

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['title', 'description']
