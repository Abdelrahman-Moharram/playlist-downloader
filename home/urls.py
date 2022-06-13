from django.urls import path
from . import views
app_name = "home"

urlpatterns = [
		path("", views.index, name="index"),
		path("report/", views.Report, name="report"),
		path("notificatins/<int:notifyId>/", views.notifications, name="notfications"),
]