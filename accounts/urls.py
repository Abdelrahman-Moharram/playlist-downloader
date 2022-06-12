from django.urls import path
from . import views
app_name = "accounts"
urlpatterns = [
    path("login/",views.login_user,name="login"),
    path("logout/",views.logout_user,name="logout"),
    path("register/",views.register,name="register"),    
    path("<str:username>",views.profile,name="profile"),    
]
