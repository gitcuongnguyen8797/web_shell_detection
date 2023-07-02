from django.urls import path
from . import views

urlpatterns = [
    path('healthy-check', views.healthy_check, name='healthy'),
    path('check-uploaded-file', views.check_upload_file, name='check-uploaded-file')
]