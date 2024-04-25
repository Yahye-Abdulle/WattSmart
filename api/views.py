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

initial_message = f'''
Act as 'WattSmart Virtual Assistant'. Respond to user queries about gas and electricity in a 20-word limit, providing conversational and professional advice." I made the following changes to make the prompt clearer and more specific for the ChatGPT model: 1. Simplified the title: Instead of a long phrase, I used a straightforward title that clearly identifies the assistant's role. 2. Focused on the main task: I removed unnecessary details and emphasized the primary objective of responding to user queries. 3. Highlighted the key constraint: The 20-word limit was moved to the forefront to ensure the model stays concise and within the specified word count. 4. Used actionable language: Phrases like "Respond to user queries" and "providing advice" give the model clear instructions on what to do.
Return responses in plain text format. No markdown syntax such as ###, **, bullet points and other syntaxs. 
Keep responses clear and concise.
No bullet points or markdown syntax.
'''

def remove_markdown(text):
    # Remove bold formatting: **text**
    text = re.sub(r'\*\*(.*?)\*\*', '', text)
    
    # Remove italic formatting: *text*
    text = re.sub(r'\*(.*?)\*', '', text)
    
    # Remove headers: ### text
    text = re.sub(r'###(.*?)\n', r'\1\n', text)
    text = re.sub(r'##(.*?)\n', r'\1\n', text)
    text = re.sub(r'#(.*?)\n', r'\1\n', text)
    
    # Remove code blocks: ```code```
    text = re.sub(r'```(.*?)```', '', text)
    
    # Remove inline code: `code`
    text = re.sub(r'`(.*?)`', '', text)
    
    # Remove unordered lists: - item
    text = re.sub(r'- (.*?)\n', '', text)
    
    # Remove ordered lists: 1. item
    text = re.sub(r'\d+\.(.*?)\n', '', text)
    
    # Remove links: [text](url)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1', text)
    
    # Remove blockquotes: > text
    text = re.sub(r'> (.*?)\n', '', text)
    
    # Remove horizontal rules: ---
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
        
        # Fetch or create user's conversation history
        user_conversation_history, created = UserConversationHistory.objects.get_or_create(user=request.user)
        conversation_history = user_conversation_history.conversation_history
        
        user = request.user
        if not user.has_setup:
            conversation_history.append({'role': 'user', 'content': initial_message})
            user.has_setup = True
            user.save()
        
        conversation_history.append({'role': 'user', 'content': message})
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
        
        if response.choices:
            # ai_response = remove_markdown(response.choices[0].message.content)
            ai_response = response.choices[0].message.content
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
        # Fetch user's conversation history from the database
        user_conversation_history, created = UserConversationHistory.objects.get_or_create(user=request.user)
        conversation_history = user_conversation_history.conversation_history
        return JsonResponse({'conversation_history': conversation_history})
    else:
        return JsonResponse({'error': 'User is not authenticated.'}, status=401)

# @csrf_exempt
# def gptResponses(request: HttpRequest) -> JsonResponse:
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             message = data.get('message')
#             if message:
#                 if not isinstance(request.user, AnonymousUser):  # Check if user is authenticated
#                     user = request.user
#                     if not hasattr(user, 'has_setup'):
#                         initial_message = f'''
#                         Hello, I'm the user of this energy management system. You are to help me reduce energy usage and bills. Here are my rules and instructions for you:
                        
#                         1. Respond to me if the message I sent is appropriate for the situation. Where the situation is that I want to save energy, money, monitor my energy usage etc. If not, say message not appropriate.
#                         2. Make each response clear and concise. I prefer bullet points for easy reading.
#                         3. Focus on actionable strategies that I can implement without significant investments.
#                         4. Offer insights based on my total energy usage and cost. If there are patterns or tips relevant to saving money, include those.
#                         5. Format your response in JSON, with each response/recommendation as an item in an array.

#                         Thank you for assisting me in this effort to save energy and money.
#                         '''

#                         client.chat.completions.create(
#                             model="gpt-3.5-turbo",
#                             messages=[{
#                                 "role": "user", 
#                                 "content": initial_message
#                             }],
#                         )
                        
#                         # Mark the user as having completed the setup
#                         user.has_setup = True
#                         user.save()
                    
#                     # Create a new ChatMessage object for the user's message
#                     sender_id = request.user.id
#                     user_message = ChatMessage.objects.create(
#                         sender_id=sender_id,
#                         receiver_id=None,  # Assuming AI is the receiver
#                         message=message
#                     )
                    
#                     # Call the AI model to get the response
#                     ai_response = client.chat.completions.create(
#                         model="gpt-3.5-turbo",
#                         messages=[{"role": "user", "content": message}],
#                     )
                    
#                     # Create a new ChatMessage object for the AI's response
#                     ai_message = ChatMessage.objects.create(
#                         sender_id=None,  # Assuming AI is the sender
#                         receiver_id=sender_id,
#                         message=ai_response.choices[0].message.content
#                     )
#                     # Assuming successful response structure
#                     return JsonResponse({'message': ai_response.choices[0].message.content})
#                 else:
#                     return JsonResponse({'error': 'User is not authenticated.'}, status=401)
#             else:
#                 return JsonResponse({'error': 'Message must be provided.'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
#     else:
#         return JsonResponse({'error': 'Invalid request method.'}, status=405)

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
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            name = data.get('name')
            typeApp = data.get('type')
            # generate a random wattage
            if typeApp == 'gas':
                random_wattage = random.randint(40, 95)
            else:
                random_wattage = random.randint(100, 300)

            # Round the wattage to the nearest multiple of 100
            wattage = round(random_wattage, -2)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data.'}, status=400)
        
        if name and wattage and typeApp:
            appliance = request.user.appliances.create(name=name, wattage=wattage, type=typeApp)
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
    

# client = Client()

# def setupClientFirstTime():
#     response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": '''
#                            Hi there, I will give you data below that will consist of gas and electricity data. I want you to understand patterns
#                            and give me insights on how I can save energy. I will give you data for the past 12 months
                           
#                            gasUsage = [60, 55, 65, 85, 55, 35, 90, 85, 80, 75, 70, 85] Cost = £126
#                            electricityUsage = [312, 260, 250, 215, 180, 240, 150, 142, 200, 370, 350, 255] = £438.60
                           
#                            Recommend me ways to save energy and money.
                           
#                            I want you to keep the recommendations to max 5 and keep it short and concise. 
#                            Have it in bullet points and make sure it is easy to understand. Don't write too much
                           
#                            Return the answer in JSON format
                           
#                            '''}],
#             )
    


# @csrf_exempt
# def gptResponses(request) -> JsonResponse:
#     # check if requiest is post
#     if request.method == 'POST':
#         # get the data from the request
#         data = json.loads(request.body)
#         # get the message from the data
#         message = data.get('message')
#         # check if message is not none
#         if message:
#             response = client.chat.completions.create(
#                 model="gpt-3.5-turbo",
#                 messages=[{"role": "user", "content": '''
#                            Please answer the question below is JSON format where the response is in bullet points and easy to understand. Each element in array should be a bullet point.
#                            The message below is what you will respond to labelled with message
                           
#                            Message: ''' + message + '''
                           
#                            '''}],
#             )
#             print(response.choices[0].message.content)
#             # return the message
#             return JsonResponse({'message': response.choices[0].message.content})
#         else:
#             # return an error message
#             return JsonResponse({'error': 'Message must be provided.'}, status=400)