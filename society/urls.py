from django.urls import path
from . import views  # Import views from the current app
from .views import edit_profile
from .views import complaint_list, create_complaint, update_complaint_status
from .views import update_maintenance_status
from .views import edit_notice, delete_notice
from .views import event_list, create_event, edit_event, delete_event


urlpatterns = [
    path('membership/', views.membership_directory, name='membership_directory'),
    #path('', views.home, name='home'),
    path('add/', views.add_member, name='add_member'),
    path('edit/<int:member_id>/', views.edit_member, name='edit_member'),
    path('delete/<int:member_id>/', views.delete_member, name='delete_member'),

    path('', views.home, name='home'),  # Visitors see this page
    path('dashboard/', views.dashboard, name='dashboard'),  # Logged-in users see this



    #path('', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('accounts/logout/', views.custom_logout, name='custom_logout'),

    path('documents/', views.document_list, name='document_list'),
    path('documents/upload/', views.upload_document, name='upload_document'),
    path('documents/update/<int:pk>/', views.document_update, name='document_update'),
    path('documents/delete/<int:pk>/', views.document_delete, name='document_delete'),
    path('documents/download/<int:pk>/', views.download_document, name='download_document'),

    path('maintenance/', views.maintenance_requests, name='maintenance_requests'),
    path('maintenance/create/', views.create_maintenance_request, name='create_maintenance_request'),
    path('maintenance/update-status/<int:request_id>/', views.update_maintenance_status,name='update_maintenance_status'),

    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/edit/<int:event_id>/', edit_event, name='edit_event'),
    path('events/delete/<int:event_id>/', delete_event, name='delete_event'),

    path('notices/', views.notice_list, name='notice_list'),
    path('notices/create/', views.create_notice, name='create_notice'),
    path('notice/edit/<int:notice_id>/', edit_notice, name='edit_notice'),
    path('notice/delete/<int:notice_id>/', delete_notice, name='delete_notice'),

    path('complaints/', views.complaint_list, name='complaint_list'),
    path('complaints/create/', views.create_complaint, name='create_complaint'),
    path('complaints/update_status/<int:complaint_id>/<str:status>/', update_complaint_status, name='update_complaint_status'),
    path('complaint/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),


    path('admin/manage-users/', views.manage_users, name='manage_users'),
]