from django.shortcuts import render, redirect, get_object_or_404
from society.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import MaintenanceRequest, Event, Notice, Complaint, Document, Member, CustomUser
from .forms import MaintenanceRequestForm, EventForm, NoticeForm, ComplaintForm, DocumentForm, MemberForm, SignUpForm
from django.contrib.auth import login, logout
from django.http import FileResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from .forms import NoticeForm
from .models import Notice
from .models import Event
from .forms import EventForm
from django.shortcuts import get_object_or_404, redirect
import os


def home(request):
    template_dir = os.path.join(os.path.dirname(__file__), '../template')
    print("Template Directory Exists:", os.path.exists(template_dir))
    print("Templates:", os.listdir(template_dir) if os.path.exists(template_dir) else "Not Found")

    return render(request, 'Home.html')

@login_required
def dashboard(request):
    """Dashboard accessible only to logged-in users."""
    return render(request, 'dashboard.html')

def manage_users(request):
    users = CustomUser.objects.all()  # Fetch all custom users from the database
    return render(request, 'admin/manage_users.html', {'users': users})
# Membership Directory
# List Members
@login_required
def membership_directory(request):
    members = Member.objects.all()

    # Filter by role if specified
    if request.GET.get('role'):
        role_filter = request.GET.get('role')
        members = members.filter(role=role_filter)
    is_admin = request.user.is_admin  # or request.user.role == 'Admin'
    return render(request, 'membership_directory.html', {'members': members})

# Add Member
@login_required
def add_member(request):
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('membership_directory')
            except IntegrityError:
                form.add_error('flat_number', 'This flat number is already assigned to another member.')
    else:
        form = MemberForm()
    return render(request, 'add_member.html', {'form': form})

# Edit Member
@login_required
def edit_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            # Check if the flat number is changed and is already taken
            flat_number = form.cleaned_data.get('flat_number')
            if Member.objects.exclude(id=member.id).filter(flat_number=flat_number).exists():
                form.add_error('flat_number', 'This flat number is already assigned to another member.')
            else:
                form.save()
                return redirect('membership_directory')
    else:
        form = MemberForm(instance=member)
    return render(request, 'edit_member.html', {'form': form})
# Delete Member
@login_required
def delete_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    member.delete()
    return redirect('membership_directory')

# Document Management
@login_required
def document_list(request):
    documents = Document.objects.all()
    context = {
        'documents': documents,
    }
    return render(request, 'document_list.html', context)

@login_required
def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.save()
            return redirect('document_list')
    else:
        form = DocumentForm()
    return render(request, 'upload_document.html', {'form': form})

@login_required
def document_update(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_list')
    else:
        form = DocumentForm(instance=document)
    return render(request, 'upload_document.html', {'form': form})

# Delete Document
@login_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == 'POST':
        document.delete()
        return redirect('document_list')
    return render(request, 'document_confirm_delete.html', {'document': document})

# Download Document in Original Format
@login_required
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    response = FileResponse(document.file.open('rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{document.file.name.split("/")[-1]}"'
    return response

# Profile
@login_required
def profile(request):
    user = request.user  # Get the logged-in user
    context = {
        'username': user.username,
        'email': user.email,
        'phone_number': user.phone_number,
        'flat_number': user.flat_number,
    }
    return render(request, 'profile.html', context)

# Logout
def custom_logout(request):
    logout(request)  # Log out the user
    return redirect('login')  # Redirect to the login page

# Sign Up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = form.cleaned_data['user_type']

            if user_type == 'admin':
                user.is_admin = True
            elif user_type == 'flat_owner':
                user.is_flat_owner = True
            elif user_type == 'tenant':
                user.is_tenant = True

            # Save the user and log them in
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})

# Base Dashboard
@login_required
def dashboard(request):
    if request.user.is_admin:
        return render(request, 'admin_dashboard.html')
    elif request.user.is_flat_owner:
        return render(request, 'flat_owner_dashboard.html')
    elif request.user.is_tenant:
        return render(request, 'tenant_dashboard.html')
    else:
        return redirect('login')  # Redirect to login if no role is assigned

# Check if the user is an admin
def is_admin(user):
    return user.is_authenticated and user.is_admin

# Admin Users Management
@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users_list = CustomUser.objects.all()  # Fetch all users
    paginator = Paginator(users_list, 10)  # Show 10 users per page
    page_number = request.GET.get('page')
    users = paginator.get_page(page_number)
    context = {
        'users': users,
    }
    return render(request, 'admin/manage_users.html', context)

# Maintenance Management
def is_admin(user):
    return user.is_authenticated and user.is_admin  # Ensure your User model has `is_admin` field


@login_required
def maintenance_requests(request):
    """Allow all users to view maintenance requests."""
    requests = MaintenanceRequest.objects.all()  # Show all requests to everyone
    return render(request, 'maintenance_requests.html', {'requests': requests})

@login_required
def create_maintenance_request(request):
    """Allow all users to create a maintenance request."""
    if request.method == 'POST':
        form = MaintenanceRequestForm(request.POST)
        if form.is_valid():
            request_obj = form.save(commit=False)
            request_obj.created_by = request.user
            request_obj.save()
            return redirect('maintenance_requests')
    else:
        form = MaintenanceRequestForm()
    return render(request, 'create_maintenance_request.html', {'form': form})

@login_required
@user_passes_test(is_admin)  # Only admins can update request status
def update_maintenance_status(request, request_id):
    """Only admins can mark a request as Completed or Rejected."""
    request_obj = get_object_or_404(MaintenanceRequest, id=request_id)

    if request.method == "POST":
        status = request.POST.get("status")  # Get status from form data
        if status in ['Completed', 'Rejected']:  # Ensure valid status
            request_obj.status = status
            request_obj.save()

    return redirect('maintenance_requests')
# Event Management
@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})


@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'create_event.html', {'form': form})


@login_required
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'edit_event.html', {'form': form})


@login_required
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('event_list')

    return render(request, 'confirm_delete_event.html', {'event': event})


# Notice Board
@login_required
def notice_list(request):
    notices = Notice.objects.all()
    return render(request, 'notice_list.html', {'notices': notices})


@login_required
def create_notice(request):
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            return redirect('notice_list')
    else:
        form = NoticeForm()
    return render(request, 'create_notice.html', {'form': form})


@login_required
def edit_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        form = NoticeForm(request.POST, instance=notice)
        if form.is_valid():
            form.save()
            return redirect('notice_list')
    else:
        form = NoticeForm(instance=notice)

    return render(request, 'edit_notice.html', {'form': form})


@login_required
def delete_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)

    if request.method == 'POST':
        notice.delete()
        return redirect('notice_list')

    return render(request, 'confirm_delete_notice.html', {'notice': notice})

# Complaint Management
@login_required
def complaint_list(request):
    complaints = Complaint.objects.all()  # Fetch all complaints
    return render(request, 'complaint_list.html', {'complaints': complaints})


@login_required
def create_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.created_by = request.user
            complaint.save()
            return redirect('complaint_list')
    else:
        form = ComplaintForm()
    return render(request, 'create_complaint.html', {'form': form})


# Function to check if user is admin
def is_admin(user):
    return user.is_authenticated and user.is_admin  # Ensure your User model has `is_admin` field


@login_required
@user_passes_test(is_admin)  # Restrict to admins only
def update_complaint_status(request, complaint_id, status):
    complaint = get_object_or_404(Complaint, id=complaint_id)

    if status in ['Completed', 'Rejected']:  # Ensure valid status
        complaint.status = status
        complaint.save()

    return redirect('complaint_list')  # Redirect back to complaints page

@login_required
def edit_profile(request):
    user = request.user  # Get logged-in user
    if request.method == 'POST':
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.phone_number = request.POST.get('phone_number', '')
        user.flat_number = request.POST.get('flat_number', '')
        user.save()
        return redirect('profile')

    return render(request, 'edit_profile.html', {'user': user})


@login_required
@user_passes_test(is_admin)  # Restrict to admins only
def delete_complaint(request, complaint_id):
    complaint = get_object_or_404(Complaint, id=complaint_id)
    complaint.delete()  # This will delete the complaint
    return redirect('complaint_list')  # Redirect back to complaints list s