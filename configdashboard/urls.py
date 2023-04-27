from django.urls import path
from . import views

app_name = 'configdashboard'

urlpatterns =[path('', views.configDashboard, name="dashboard"),
              path("add_gender",views.add_gender,name="add_gender"),
              path("remove_gender/<str:gender>",views.remove_gender, name="remove_gender"),
              path("toggle_module/<str:module>/<str:name>", views.toggle_modules, name="toggle_module"),
              path("add_network", views.add_network,name="add_network"),
              path("remove_network/<str:network>",views.remove_network,name="remove_network"),
              path("add_module/",views.add_module, name="add_module"),
              path("remove_module/<str:module>",views.remove_module, name="remove_module")]
