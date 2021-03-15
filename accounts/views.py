from django.shortcuts import render,redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy,reverse
from django.contrib import messages
from .forms import CreateUserForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout

class Register(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
    
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('home'))
                else:
                   return  HttpResponse('account not active')
            else:
                messages.add_message(request, messages.ERROR, 'Username or Password is incorrect')
                return HttpResponse('Invalid login details supplied')        

        else:
            return render(request, 'registration/login.html',{})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('post_list'))