from django.http import HttpResponse, HttpRequest, JsonResponse
import json
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate, get_user_model
from .forms import RegistrationForm, CustomAuthenticationForm, SignUpForm
from .models import CustomUser, UserConversationHistory
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt
import random
from g4f.client import Client
from django.db.models import Sum
from .models import ChatMessage
from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404
import re

client = Client()

# initial_message = f'''
# Create a conversational and professional response as a "WattSmart Virtual Assistant", providing energy-related advice, recommendations, or answers to potential user questions about gas and electricity, within a 20-word limit in a text-based format. Follow these instructions strictly especially the word count."
# '''

# initial_message = f'''
# Act as 'WattSmart Virtual Assistant'. Respond to user queries about gas and electricity in a 20-word limit, providing conversational and professional advice." I made the following changes to make the prompt clearer and more specific for the ChatGPT model: 1. Simplified the title: Instead of a long phrase, I used a straightforward title that clearly identifies the assistant's role. 2. Focused on the main task: I removed unnecessary details and emphasized the primary objective of responding to user queries. 3. Highlighted the key constraint: The 20-word limit was moved to the forefront to ensure the model stays concise and within the specified word count. 4. Used actionable language: Phrases like "Respond to user queries" and "providing advice" give the model clear instructions on what to do.
# Return responses in plain text format. No markdown syntax such as ###, **, bullet points and other syntaxs. 
# Keep responses clear and concise.
# No bullet points or markdown syntax.
# '''

# initial_message = "Act as 'Chat Assistant,' strictly respond to energy-related queries in 30 words maximum, offering professional advice. Take every input as a question!"

initial_message = "I want you to be an energy expert AI that only answer questions relevant to the energy sector. When you answer, respond in a way that a non-energy person will understand. Call yourself Chat Assistant"

# I will give examples below. There will be two people in this situation (Human and Computer)
# You are Computer and Human is asking the questions

# Human: What time is it best to reduce energy usage?
# Computer: The best time to reduce energy usage is during off-peak hours, typically early morning or late at night.

# Human: How can I reduce my energy consumption at home?
# Computer: Use LED bulbs, unplug electronics when not in use, and upgrade to energy-efficient appliances to reduce energy consumption at home.

# Human: Who is the best football player in the world?
# Computer: I'm sorry, I can only provide information on energy-related queries. Please ask a question related to energy usage or conservation.

# These are simply examples. You can use them as a guide to help you understand the task. Do not respond as the formats.

def remove_markdown(text):
    text = re.sub(r'\*\*(.*?)\*\*', '', text)
    text = re.sub(r'\*(.*?)\*', '', text)
    text = re.sub(r'###(.*?)\n', r'\1\n', text)
    text = re.sub(r'##(.*?)\n', r'\1\n', text)
    text = re.sub(r'#(.*?)\n', r'\1\n', text)
    text = re.sub(r'```(.*?)```', '', text)
    text = re.sub(r'`(.*?)`', '', text)
    text = re.sub(r'- (.*?)\n', '', text)
    text = re.sub(r'\d+\.(.*?)\n', '', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    text = re.sub(r'> (.*?)\n', '', text)
    text = re.sub(r'---', '', text)
    return text

@csrf_exempt
def gptResponses(request: HttpRequest) -> JsonResponse:
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method.'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    
    try:
        data = json.loads(request.body)
        message = data.get('message')
        
        if not message:
            return JsonResponse({'error': 'Message must be provided.'}, status=400)
        
        user_conversation_history, created = UserConversationHistory.objects.get_or_create(user=request.user)
        conversation_history = user_conversation_history.conversation_history
        
        user = request.user
        if not user.has_setup:
            conversation_history.append({'role': 'user', 'content': initial_message})
            user.has_setup = True
            user.save()
        
        conversation_history.append({'role': 'user', 'content': message})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo", #gpt-4-32k-0613
            messages=[{"role": "user", "content": '''
            instructions: ''' + initial_message + '''
            
            question: ''' + message + '''
            
            Answer in 30 word maximum and keep the response clear and concise.
            If question is not relevant to energy sector, respond with a message that the question is not relevant.
            Return the answer only
            '''}]
            #conversation_history
        )
        if response.choices:
            ai_response = remove_markdown(response.choices[0].message.content).strip()
            conversation_history.append({'role': 'ai', 'content': ai_response})
            user_conversation_history.conversation_history = conversation_history
            user_conversation_history.save()
            return JsonResponse({'message': ai_response})
        else:
            return JsonResponse({'error': 'No response from AI model.'}, status=500)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def get_conversation_history(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        user_conversation_history, created = UserConversationHistory.objects.get_or_create(user=request.user)
        conversation_history = user_conversation_history.conversation_history
        return JsonResponse({'conversation_history': conversation_history})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

def check_auth(request) -> JsonResponse:
    if request.user.is_authenticated:
        return JsonResponse({'authenticated': True})
    else:
        return JsonResponse({'authenticated': False})
    
def get_appliances_for_user(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        appliances = request.user.appliances.all()
        appliances = appliances.order_by('wattage').reverse()
        return JsonResponse({'appliances': list(appliances.values())})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)


appliances = [
    {'name': 'Toaster', 'type': 'electricity', 'min_wattage': 600, 'max_wattage': 1200},
    {'name': 'Microwave', 'type': 'electricity', 'min_wattage': 800, 'max_wattage': 2000},
    {'name': 'Oven', 'type': 'electricity', 'min_wattage': 1500, 'max_wattage': 5000},
    {'name': 'Stove', 'type': 'gas', 'min_wattage': 40, 'max_wattage': 95},
    {'name': 'Gas Heater', 'type': 'gas', 'min_wattage': 100, 'max_wattage': 300},
    {'name': 'Dishwasher', 'type': 'electricity', 'min_wattage': 1200, 'max_wattage': 2000},
    {'name': 'Washing Machine', 'type': 'electricity', 'min_wattage': 500, 'max_wattage': 1500},
    {'name': 'Dryer', 'type': 'electricity', 'min_wattage': 1000, 'max_wattage': 5000},
    {'name': 'Refrigerator', 'type': 'electricity', 'min_wattage': 100, 'max_wattage': 800},
    {'name': 'Freezer', 'type': 'electricity', 'min_wattage': 100, 'max_wattage': 500},
    {'name': 'Air Conditioner', 'type': 'electricity', 'min_wattage': 1000, 'max_wattage': 5000},
    {'name': 'Space Heater', 'type': 'electricity', 'min_wattage': 500, 'max_wattage': 1500},
    {'name': 'Coffee Maker', 'type': 'electricity', 'min_wattage': 800, 'max_wattage': 1500},
    {'name': 'Blender', 'type': 'electricity', 'min_wattage': 300, 'max_wattage': 1000},
    {'name': 'Electric Grill', 'type': 'electricity', 'min_wattage': 1000, 'max_wattage': 2000},
    {'name': 'Hair Dryer', 'type': 'electricity', 'min_wattage': 800, 'max_wattage': 1800},
    {'name': 'TV', 'type': 'electricity', 'min_wattage': 50, 'max_wattage': 400},
    {'name': 'Laptop', 'type': 'electricity', 'min_wattage': 30, 'max_wattage': 150},
    {'name': 'Desktop Computer', 'type': 'electricity', 'min_wattage': 150, 'max_wattage': 600},
    {'name': 'Router', 'type': 'electricity', 'min_wattage': 5, 'max_wattage': 20},
    {'name': 'Printer', 'type': 'electricity', 'min_wattage': 20, 'max_wattage': 100},
    # Add more appliances as needed
]


@csrf_exempt
def add_appliance(request: HttpRequest) -> JsonResponse:
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        
        user_appliances = request.user.appliances.values_list('name', flat=True)
        
        num_appliances = random.randint(7, 10)
        
        selected_appliances = random.sample(appliances, num_appliances)

        for appliance in selected_appliances:
            name = appliance['name']
            typeApp = appliance['type']
            min_wattage = appliance['min_wattage']
            max_wattage = appliance['max_wattage']

            # Check if appliance already exists in user's list
            if name not in user_appliances:
                # Generate a random wattage within the specified range
                if typeApp == 'gas':
                    random_wattage = random.randint(min_wattage, max_wattage)
                else:
                    random_wattage = random.randint(min_wattage, max_wattage)

                # Round the wattage to the nearest multiple of 100
                wattage = round(random_wattage, -2)

                # Create the appliance for the user
                request.user.appliances.create(name=name, wattage=wattage, type=typeApp)

        return JsonResponse({'message': 'Appliances added successfully.'})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)
    
@csrf_exempt
def delete_appliance(request, name):
    if request.method == 'DELETE':
        appliance = get_object_or_404(request.user.appliances, name=name)
        appliance.delete()
        return JsonResponse({'message': 'Appliance deleted successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)
    
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
    return redirect('/') 
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
                return redirect('/')
            else:
                # Handle invalid login credentials
                error_message = "Invalid login credentials. Please try again."
                return render(request, 'login.html', {'error_message': error_message})