from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

import bcrypt

# Landing Page
def index(request):
    context = {
        'logged_in_users' : User.objects.all()
    }
    return render(request, "login_and_registration_app/index.html", context)

#Register User
def register(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        plain_text_password = request.POST['password']
        plain_text_conf_password = request.POST['confirmation_password']

        #Hash the plaintext password created
        hashed_password = bcrypt.hashpw(plain_text_password.encode(), bcrypt.gensalt())

        #If hashed password matches confirmation password, add user to db and move to success page
        if bcrypt.checkpw(plain_text_conf_password.encode(), hashed_password):
            #Add user to database if registration successful
            new_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
            
            #Set session user_key to id
            request.session['active_user'] = new_user.id
            print(request.session['active_user'])

            return redirect('/success')
        else:
            return redirect('/')

#Login User
def login(request):
    if request.method == "POST":
        print("Request.Method == POST")
        user_email = request.POST['email']
        user_password = request.POST['password']

        login_user = User.objects.get(email=user_email)
        login_user_password = request.POST['password']

        passwords_match = bcrypt.checkpw(login_user_password.encode(), login_user.password.encode())
        if passwords_match:
            request.session['active_user'] = login_user.id
            print("Current user updated to: " + str(login_user.first_name) + str(login_user.last_name))
            return redirect('/success')
        else:
            print("Invalid credentials")
            return redirect('/')

    #Set session user_key to id
    return redirect('/success')

#Successful Login/Register
def success(request):
    if not 'active_user' in request.session:
        return redirect('/')
    
    context = {
        'current_user' : User.objects.get(id=request.session['active_user'])
    }

    print("Reached success page")
    return render(request, "login_and_registration_app/success.html", context)

#Logout User
def logout(request):
    del request.session['active_user']
    return redirect('/')