from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from home.models import Video


def login_user(request):
        if request.method == "POST":
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request,username=username,password=password)
                if user is not None:
                        login(request, user)                                
                        request.session['id'] = user.id
                        request.session['first_name'] = user.first_name
                        request.session['last_name'] = user.last_name
                        request.session['email'] = user.email
                        request.session['username'] = user.username
                        request.session['is_superuser'] = user.is_superuser
                        request.session['date'] = str(user.date_joined)
                        if user.is_superuser:
                                return redirect("/admin/")
                        else:
                                return redirect("home:index")
                else:
                        messages.warning(request,"Can't Login E-Mail or Password are invalid",extra_tags="danger")

        return render(request,'accounts/login.html', {})

def register(request):
        if request.method == "POST":
                if request.POST['password'] == request.POST['confirm_password']:
                        user = User.objects.create_user(username=request.POST['username'],email=request.POST['email'],password=request.POST['password'])
                        user.first_name = request.POST['first_name']
                        user.last_name = request.POST['last_name']
                        user.save()
                        username = request.POST['username']
                        password = request.POST['password']
                        user = authenticate(request,username=username,password=password)
                        if user is not None:
                                login(request, user)
                                request.session['id'] = user.id
                                request.session['first_name'] = user.first_name
                                request.session['last_name'] = user.last_name
                                request.session['email'] = user.email
                                request.session['username'] = user.username
                                request.session['is_superuser'] = user.is_superuser
                                messages.success(request,"Your Data has Saved!",extra_tags="success")
                                return redirect("home:index")
                        else:
                                messages.warning(request,"Error while signing you in but your data has Saved!",extra_tags="danger")
                                return redirect("home:index")
                else:
                        messages.warning(request,"Password Not The Same",extra_tags="warning")
        return render(request,'accounts/register.html', {})

@login_required
def logout_user(request):
        logout(request)
        return redirect("home:index")


@login_required
def profile(request, username):
        user = User.objects.get(username=username)
        if request.user == user:
                return render(request, 'accounts/profile.html', {"videos":Video.objects.filter(user=request.user)})
