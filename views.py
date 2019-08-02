from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from customuser.models import user_type, User

def signup(request):
    if (request.method == 'POST'):
        email = request.POST.get('email')
        password = request.POST.get('password')
        st = request.POST.get('student')
        te = request.POST.get('teacher')
        
        user = User.objects.create_user(
            email=email,
        )
        user.set_password(password)
        user.save()
        
        usert = None
        if st:
            usert = user_type(user=user,is_student=True)
        elif te:
            usert = user_type(user=user,is_teach=True)
        
        usert.save()
        #Successfully registered. Redirect to homepage
        return redirect('home')
    return render(request, 'register.html')
    
def login(request):
    if (request.method == 'POST'):
        email = request.POST.get('email') #Get email value from form
        password = request.POST.get('password') #Get password value from form
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            type_obj = user_type.objects.get(user=user)
            if user.is_authenticated and type_obj.is_student:
                return redirect('shome') #Go to student home
            elif user.is_authenticated and type_obj.is_teach:
                return redirect('thome') #Go to teacher home
        else:
            # Invalid email or password. Handle as you wish
            return redirect('home')

    return render(request, 'home.html')