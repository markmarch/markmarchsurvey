from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.messages.api import get_messages
from django.core.context_processors import csrf

from django.contrib.auth.models import User

from forms import *

def signin(request):
    """Login View"""
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect("/home")
                else:
                    return HttpResponseRedirect("")
            else:
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append(u"Invalid username or password")
        return render_to_response('signin.html', {"form": form}, 
            context_instance=RequestContext(request))
    else:
        return render_to_response('signin.html', Request_instance=RequestContext(request))
    

def home(request):
    """Home view, displays login mechanism"""
    return render_to_response('home.html',RequestContext(request))

def signup(request):
    """Sign up view, display sign up page"""
    c = {}
    c.update(csrf(request))
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            if user is not None:
                user = authenticate(username=cd['username'], password=cd['password'])
                login(request, user)
                return HttpResponseRedirect("/account/edit/")
            else:
                return HttpResponseRedirect("/signup/")
    else:
        form = SignUpForm()
    return render_to_response('signup.html', {
        'form': form
    }, context_instance=RequestContext(request))

@login_required
def done(request):
    """Login complete view, displays user data"""
    return render_to_response('home.html', RequestContext(request))

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'messages': messages},
                              RequestContext(request))

def signout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')