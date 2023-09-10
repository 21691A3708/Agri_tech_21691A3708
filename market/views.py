from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,bUpdateProfileForm,fUpdateProfileForm
from .forms import ProductionForm
from .models import Production
from django.shortcuts import render, get_object_or_404
from .models import CustomUser, Production 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Production
from .models import CustomUser, Chat
from .forms import ChatForm  
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.shortcuts import render, get_object_or_404
from .forms import MessageForm
from .models import Chat
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Chat, Message
from django.core.mail import EmailMessage,send_mail
from Agri_Tech import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import activate, get_language
User = get_user_model()



def home(request):
    
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    return render(request, 'home/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            role = request.POST.get('role_type')
            user = form.save()
            chat = Chat.objects.create()
            chat.participants.add(user)
            chat.save()
            #email Function
            fn=user.first_name+" "+user.last_name
            send_welcome_email(user.email,fn)
            messages.success(request, 'Your have successfully signup!')
            #CustomUser.objects.create(user=user, role_type=role)
            # Additional processing if needed, such as sending a confirmation email
            return redirect('signin')  # Redirect to the login page after successful signup
    else:
        form = SignUpForm()
        messages.success(request, 'Fill the form correctly !')
    return render(request, 'home/signup.html', {'form': form})

def send_welcome_email(user_email, user_first_name):
    subject = 'Welcome to AgriTech!'
    html_message = render_to_string('welcome_email.html', {'user': user_first_name})
    message = ''
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role_type == 'farmer':
                    if user.last_login is None:
                        print("hello")
                    #fn= request.user.first_name+" "+request.user.last_name
                    #send_first_time_login_email(request.user.email,fn)
                    messages.success(request, 'Your have successfully signin!')
                    return redirect('farmer_home') 
                elif user.role_type == 'buyer':
                    if user.last_login is None:
                        print("hello")
                    #fn= request.user.first_name+" "+request.user.last_name
                    #send_first_time_login_email(request.user.email,fn)
                    messages.success(request, 'Your have successfully signin!')                    
                    return redirect('buyer_home')
    else:
        messages.success(request, 'Fill the correct delatils')
        form = AuthenticationForm(request)
    return render(request, 'home/signin.html', {'form': form})


def send_first_time_login_email(user_email, user_first_name):
    subject = 'Welcome to AgriTech - First-Time Login'
    html_message = render_to_string('first_time_login_email.html', {'user': user_first_name})
    message = ''
    from_email =settings.EMAIL_HOST_USER
    recipient_list = [user_email]

    send_mail(subject, message, from_email, recipient_list, html_message=html_message)

@login_required
def signout(request):
    logout(request)
    messages.success(request, 'Your have successfully signout!')
    return redirect('signin') 




@login_required
def chat(request):
    # Retrieve and display the user's chats
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'chat/chat_list.html', {'chats': chats})


@login_required
def chat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = Message.objects.filter(chat=chat)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['message']
            Message.objects.create(chat=chat, sender=request.user, content=content)
            # Redirect to the chat room after sending the message
            return redirect('chat_room', chat_id=chat_id)
    else:
        form = MessageForm()

    return render(request, 'chat/chat_room.html', {'chat': chat, 'messages': messages, 'form': form})
#Farmers................................................................................

@login_required
def farmer_home(request):
    return render(request, 'farmer/farmer_home.html')

@login_required
def fupdate_profile(request):
    user = request.user

    if request.method == 'POST':
        form = fUpdateProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('farmer_home')
    else:
        form = fUpdateProfileForm(instance=user)
        messages.success(request, 'Fill the delatils  Propely !')
    context = {'form': form}
    return render(request, 'farmer/fupdate_profile.html', context)

@login_required
def buyer_list(request):
    buyers = CustomUser.objects.filter(role_type='buyer')  # Assuming 'role_type' is the field for user roles
    context = {'buyers': buyers}
    return render(request, 'farmer/buyer_list.html', context)

@login_required
def buyer_profile(request, username):
    buyer = get_object_or_404(CustomUser, username=username, role_type='buyer')
    context = {'buyer': buyer}
    return render(request, 'farmer/buyer_profile.html', context)


@login_required
def add_production(request):
    if request.method == 'POST':
        form = ProductionForm(request.POST, request.FILES)
        if form.is_valid():
            production = form.save(commit=False)
            production.farmer = request.user
            production.save()
            messages.success(request, 'Your production have  been added the successfully!')
            return redirect('farmer_productions')
    else:
        form = ProductionForm()
        messages.success(request, 'Enter the production delatils correctly!')
    context = {'form': form}
    return render(request, 'farmer/add_production.html', context)

@login_required
def farmer_productions(request):
    productions = Production.objects.filter(farmer=request.user)
    context = {'productions': productions}
    return render(request, 'farmer/farmer_productions.html', context)


@login_required
def edit_production(request, pk):
    production = get_object_or_404(Production, pk=pk, farmer=request.user)

    if request.method == 'POST':
        form = ProductionForm(request.POST, request.FILES, instance=production)
        if form.is_valid():
            form.save()
            messages.success(request, 'edit production done successfully!')
            return redirect('farmer_productions')
    else:
        form = ProductionForm(instance=production)
        messages.success(request, 'now your editing the production!')
    context = {'form': form, 'production': production}
    return render(request, 'farmer/edit_production.html', context)

@login_required
def delete_production(request, pk):
    production = get_object_or_404(Production, pk=pk, farmer=request.user)
    if request.method == 'POST':
        production.delete()
        messages.success(request, 'your production has been deleted !')
        return redirect('farmer_productions')
    
    context = {'production': production}
    return render(request, 'farmer/delete_production.html', context)


@login_required
def production_detail(request, pk):
    production = get_object_or_404(Production, pk=pk)
    context = {'production': production}
    return render(request, 'farmer/production_detail.html', context)


#Buyers section.................................................................................................
@login_required
def buyer_home(request):
    return render(request, 'buyer/buyer_home.html')


@login_required
def bupdate_profile(request):
    user = request.user

    if request.method == 'POST':
        form = bUpdateProfileForm(request.POST, request.FILES,  instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('buyer_home')
    else:
        form = bUpdateProfileForm(instance=user)
    context = {'form': form}
    return render(request, 'buyer/bupdate_profile.html', context)

@login_required
def farmers_list(request):
    farmers = CustomUser.objects.filter(role_type='farmer')
    context = {'farmers': farmers}
    return render(request, 'buyer/farmers_list.html', context)


@login_required
def farmer_profile(request, username):
    farmer = get_object_or_404(CustomUser, username=username, role_type='farmer')
    productions = Production.objects.filter(farmer=farmer)
    context = {'farmer': farmer, 'productions': productions}
    return render(request, 'buyer/farmer_profile.html', context)

#production list 
@login_required
def bproduction_list(request, username):
    farmer = get_object_or_404(CustomUser, username=username, role_type='farmer')
    productions = Production.objects.filter(farmer=farmer)
    context = {'farmer': farmer, 'productions': productions}
    return render(request, 'buyer/bproduction_list.html', context)


@login_required
def bproduction_detail(request, pk):
    production = get_object_or_404(Production, pk=pk)
    context = {'production': production}
    return render(request, 'buyer/bproduction_detail.html', context)


@login_required
def purchases(request):
    return render(request, 'buyer/purchases.html')

@login_required
def payment_history(request):
    return render(request, 'buyer/payment_history.html')

@login_required
def fchange_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session with new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signin')  # Replace 'buyer_dashboard' with your actual dashboard URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'farmer/change_password.html', {'form': form})

@login_required
def bchange_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update session with new password
            messages.success(request, 'Your password was successfully updated!')
            return redirect('signin')  # Replace 'buyer_dashboard' with your actual dashboard URL
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'buyer/change_password.html', {'form': form})

@login_required
def bchat(request):
    # Retrieve and display the user's chats
    chats = Chat.objects.filter(participants=request.user)
    return render(request, 'buyers/bchat_list.html', {'chats': chats})

def bchat_room(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)
    messages = chat.messages.order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['message']
            Message.objects.create(chat=chat, sender=request.user, content=content)

    else:
        form = MessageForm()

    return render(request, 'buyer/bchat_room.html', {'chat': chat, 'messages': messages, 'form': form})

