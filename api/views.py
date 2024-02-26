from django.http import HttpResponse, HttpRequest, JsonResponse
import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from .forms import RegistrationForm, CustomAuthenticationForm, SignUpForm
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt


def check_auth(request) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})
    
def get_appliances_for_user(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        appliances = request.user.appliances.all()
        return JsonResponse({'appliances': list(appliances.values())})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

@csrf_exempt
def add_appliance(request: HttpRequest) -> JsonResponse:
    print('yes')
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            name = data.get('name')
            wattage = data.get('wattage')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        
        if name and wattage:
            appliance = request.user.appliances.create(name=name, wattage=wattage)
            return JsonResponse({'appliance': {'name': appliance.name, 'wattage': appliance.wattage}})
        else:
            return JsonResponse({'error': 'Name and wattage must be provided.'}, status=400)
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    
def get_energy_usage_for_user(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        energy_usage = request.user.energy_usage.all()
        return JsonResponse({'energy_usage': list(energy_usage.values())})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_profile = CustomUser.objects.get(username=username)
                login(request, user)
                return redirect('/?email=' + user_profile.email) 
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')  # Redirect to the home page or any other desired page

def signup_view(request):
    if request.method == 'POST':
        if "signup" in request.POST:
            try:
                # Get values from request.POST
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                email = request.POST.get('email')
                password = request.POST.get('password')
                age = request.POST.get('age')

                # Ensure all required fields are provided
                if not (first_name and last_name and email and password and age):
                    raise ValueError("All required fields must be provided.")

                # Hash the password
                hashed_password = make_password(password)

                # Create a new CustomUser
                user = CustomUser.objects.create(
                    username=email,  # You can use email as the username
                    password=hashed_password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    age=age
                )

                # Log in the user
                login(request, user)

                # Redirect to a success page or wherever you want
                return redirect('/')

            except Exception as e:
                # Handle exceptions, log the error, or return an error response
                print(f"Error during signup: {e}")
                return HttpResponse("Error during signup. Please try again.")
        elif "login" in request.POST:
            email = request.POST.get('email')  # Assuming 'email' is used for the username
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Log in the user
                login(request, user)

                # Redirect to a success page or wherever you want
                user_profile = CustomUser.objects.get(username=email)
                # return redirect('/?email=' + user_profile.email)
                return redirect('/')
            else:
                # Handle invalid login credentials
                error_message = "Invalid login credentials. Please try again."
                return render(request, 'login.html', {'error_message': error_message})


    # return render(request, 'signup.html', {'form': form})