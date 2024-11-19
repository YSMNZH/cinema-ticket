from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from .models import CustomUser 
from django.contrib.auth import login as auth_login  # Make sure to import it like this
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.utils.crypto import get_random_string
from .forms import RegisterForm



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('profile') 
        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.password = form.cleaned_data['password']  # Hashing handled in form
                user.save()

                messages.success(request, "Registration successful!")
                return redirect('login')  # Replace 'login' with the name of your login route
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()

    return render(request, 'users/register.html', {'form': form})

def profile(request):
    return render(request, 'users/profile.html')





from django.shortcuts import render
from django.http import JsonResponse

def ForgotPassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        customer = CustomUser.objects.filter(email=email).first() 

        

        if customer :
            print("-----------------")
            print(customer)   
            print("-----------------")
            token = get_random_string(64)

            print(token)
            # expires_at = now() + timedelta(hours=1)


        else :
            print("user not found")    




        return JsonResponse({'status': 'success', 'message': f'Password reset email sent to {email}'})












# # -------------------------------------    
# def request_password_reset(request):


#     if request.method == 'POST':
#         email = request.POST.get('email')

#         print(email)

#         user = Users.objects.filter(email=email).first()
#         print(user)

#         if user:
#             token = get_random_string(64)
#             expires_at = now() + timedelta(hours=1)
            
#             PasswordResetTokens.objects.create(user_id=user.id, token=token, expires_at=expires_at)
            
#             reset_link = f"http://localhost:8000/reset-password/{token}"  # لینک بازنشانی رمز عبور
#             # send_mail(
#             #     'Password Reset Request',
#             #     f'Use the following link to reset your password: {reset_link}',
#             #     'no-reply@yourdomain.com', 
#             #     [email],
#             # )
#             return JsonResponse({'status': 'success', 'message': 'Password reset email sent.'})
#         return JsonResponse({'status': 'error', 'message': 'Email not found.'})
    


# def reset_password(request, token):
#     if request.method == 'POST':
#         new_password = request.POST.get('password')
#         reset_token = get_object_or_404(PasswordResetTokens, token=token)
        
#         if reset_token.expires_at < now():
#             return JsonResponse({'status': 'error', 'message': 'Token has expired.'})
        
#         user = reset_token.user
#         user.password_hash = new_password 
#         user.save()
        
#         reset_token.delete()
        
#         return JsonResponse({'status': 'success', 'message': 'Password updated successfully.'})
        
#     return render(request, 'reset_password_form.html', {'token': token})
