from django.urls import path
from . import views

app_name = 'demoupload'

urlpatterns =[path('', views.UploadExcel, name="uploadexcel")]