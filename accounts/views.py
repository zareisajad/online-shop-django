from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.db import IntegrityError
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from django.http import JsonResponse

from dashboard.views import is_manager
from .forms import UserRegistrationForm, UserLoginForm, ManagerLoginForm, EditProfileForm, SignUpForm
from accounts.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from .utils import send_verification_code
import random


def create_manager():
    """
    to execute once on startup:
    this function will call in online_shop/urls.py
    """
    if not User.objects.filter(email="manager@example.com").first():
        user = User.objects.create_user(
            "manager@example.com", 'shop manager' ,'managerpass1234'
        )
        # give this user manager role
        user.is_manager = True
        user.save()


@csrf_protect
def manager_login(request):
    if request.method == 'POST':
        form = ManagerLoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, phone_number=data['phone_number'], password=data['password']
            )
            if user is not None and user.is_manager:
                login(request, user)
                return redirect('dashboard:products')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:manager_login')
    else:
        form = ManagerLoginForm()
    context = {'form': form}
    return render(request, 'manager_login.html', context)


@csrf_protect
def user_register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.create_user(
                data['email'], data['full_name'], data['password']
            )
            return redirect('accounts:user_login')
    else:
        form = UserRegistrationForm()
    context = {'title':'Signup', 'form':form}
    return render(request, 'register.html', context)


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():

            data = form.cleaned_data
            print(f'data is : {data}')
            user = authenticate(
                request, phone_number=data['phone_number'], password=data['password']
            )

            if user is not None:
                login(request, user)
                return redirect('shop:home_page')
            else:
                messages.error(
                    request, 'username or password is wrong', 'danger'
                )
                return redirect('accounts:user_login')
    else:
        print("eeeeeeeeeeroooooreeeeeeeeeee")
        form = UserLoginForm()
    context = {'title':'Login', 'form': form}
    return render(request, 'login.html', context)


def user_logout(request):
    logout(request)
    return redirect('shop:home_page')


@csrf_protect
def edit_profile(request):
    form = EditProfileForm(request.POST, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Your profile has been updated', 'success')
        return redirect('accounts:edit_profile')
    else:
        form = EditProfileForm(instance=request.user)
    context = {'title':'Edit Profile', 'form':form}
    return render(request, 'edit_profile.html', context)

@csrf_protect
def verify_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('code')
        stored_code = request.session.get('verification_code')
        phone_number = request.session.get('phone_number')
        
        print(f"Received code: {user_code}, Stored code: {stored_code}")

        if not phone_number or not stored_code:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'Session expired. Please try again.', 'redirect_url': '/accounts/signup/'})
            return redirect('accounts:signup')  # Prevent direct access without session data

        if user_code == stored_code:
            # Mark phone as verified and move to password setup
            request.session['verified_phone'] = phone_number
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/accounts/set_password/'})
            return redirect('accounts:set_password')
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid code'})
        return render(request, 'verify_code.html', {'error': 'Invalid code'})
    
    return render(request, 'verify_code.html')



@csrf_protect
def set_password(request):
    phone_number = request.session.get('verified_phone')
    if not phone_number:
        return redirect('accounts:signup')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        is_manager = bool(request.POST.get('is_manager'))
        print(f"us :{is_manager}")
        error = None

        try:
            # Validate passwords
            if password != password_confirm:
                raise ValidationError("Passwords do not match")
                
            validate_password(password)

            # Create user properly
            user = User.objects.create_user(
                phone_number=phone_number,
                password=password,  # Django auto-hashes
                is_verify=True,
                is_active=True,
                is_manager=is_manager,
                # username=phone_number  # Uncomment if needed
            )

            request.session.flush()
            login(request, user)
            return redirect('shop:home_page')

        except ValidationError as e:
            error = e.messages[0] if e.messages else "Invalid password"
        except IntegrityError:
            error = "Account already exists with this phone number"
        except Exception as e:
            error = f"Registration error: {str(e)}"
            # Log this error for debugging: logger.error(e)

        return render(request, 'set_password.html', {
            'error': error,
            'phone_number': phone_number
        })

    return render(request, 'set_password.html', {'phone_number': phone_number})


@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['full_phone_number'])
            verification_code = str(random.randint(1000, 9999))  # Generate a 4-digit code
            # Save phone number and verification code in session
            request.session['phone_number'] = phone_number
            request.session['verification_code'] = verification_code
            print(f'storecode is :{verification_code}')
            request.session.set_expiry(600)
            send_verification_code(str(phone_number), verification_code) 
            return redirect('accounts:verify_code')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@csrf_protect
def reset_password(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            phone_number = str(form.cleaned_data['full_phone_number'])
            verification_code = str(random.randint(1000, 9999))  # Generate a 4-digit code
            # Save phone number and verification code in session
            request.session['phone_number'] = phone_number
            request.session['verification_code'] = verification_code
            print(f'storecode is :{verification_code}')
            request.session.set_expiry(600)
            send_verification_code(str(phone_number), verification_code)
            return redirect('accounts:verify_reset_code')
    else:
        form = SignUpForm()
    return render(request, 'reset_password.html', {'form': form})


@csrf_protect
def verify_reset_code(request):
    if request.method == 'POST':
        user_code = request.POST.get('code')
        stored_code = request.session.get('verification_code')
        phone_number = request.session.get('phone_number')

        if not phone_number or not stored_code:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'error': 'جلسه منقضی شده است. دوباره تلاش کنید.', 'redirect_url': '/accounts/reset_password/'})
            return redirect('accounts:reset_password')

        if user_code == stored_code:
            request.session['verified_phone'] = phone_number
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/accounts/set_new_password/'})
            return redirect('accounts:set_new_password')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'کد وارد شده صحیح نیست'})
        return render(request, 'verify_reset_code.html', {'error': 'کد وارد شده صحیح نیست'})

    return render(request, 'verify_reset_code.html')


@csrf_protect
def set_new_password(request):
    phone_number = request.session.get('verified_phone')
    if not phone_number:
        return redirect('accounts:signup')

    if request.method == 'POST':
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        error = None

        try:
            # Validate passwords
            if password != password_confirm:
                raise ValidationError("Passwords do not match")

            validate_password(password)

            user_exists = User.objects.filter(phone_number=phone_number).exists()

            if user_exists:
                # Update existing user's password
                user = User.objects.get(phone_number=phone_number)
                user.set_password(password)
                user.save()
            else:
                print('user ')


            request.session.flush()
            login(request, user)
            return redirect('shop:home_page')

        except ValidationError as e:
            error = e.messages[0] if e.messages else "Invalid password"
        except IntegrityError:
            error = "Account already exists with this phone number"
        except Exception as e:
            error = f"Registration error: {str(e)}"
            # Log this error for debugging: logger.error(e)

        return render(request, 'set_new_password.html', {
            'error': error,
            'phone_number': phone_number
        })

    return render(request, 'set_new_password.html', {'phone_number': phone_number})

