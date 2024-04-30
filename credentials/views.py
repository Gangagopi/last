

# Create your views here.


# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .forms import UserProfileForm

# Create your views here.
def login(request):
    if request.method =='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"invalid credentials")
            return redirect('login')


    return render(request,"login.html")
def register(request):
    if request.method== 'POST':
        username=request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['password1']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                 messages.info(request,"Username Taken")
                 return redirect('register')



            elif User.objects.filter(email=email).exists():
                messages.info(request, "email Taken")
                return redirect('register')

            else:
                 user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)

            user.save();
            messages.success(request, "Registration successful. Please log in.")
            return redirect('login')

        else:
            messages.info(request,"password not matching")
            return redirect('register')
        return redirect('/')


    return render(request,'register.html')
def logout(request):
    auth.logout(request)
    return redirect('/')




@login_required
def user_profile(request):
    user = request.user
    form = UserProfileForm(instance=user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('user_profile')

    return render(request, 'user_profile.html', {'user': user, 'form': form})


