from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.messages.api import get_messages
from django.core.context_processors import csrf
import urllib, hashlib
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
                    return HttpResponseRedirect("/")
                else:
                    return HttpResponseRedirect("/")
            else:
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append(u"Invalid username or password")
        return render_to_response('accounts/signin.html', {"form": form}, 
            context_instance=RequestContext(request))
    else:
        form = SignInForm()
        return render_to_response('accounts/signin.html', {"form": form},
            context_instance=RequestContext(request))

@login_required(login_url='/accounts/signin/')
def profile(request):
    """User Profile page"""
    user = request.user
    profile = user.profile
    default = "http://www.gravatar.com/avatar/"
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            user.email = cd['email']
            gravatar = "http://www.gravatar.com/avatar/"+hashlib.md5(user.email.lower()).hexdigest()+"?"
            gravatar += urllib.urlencode({'d': default, 's':str(40)})
            
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']

            profile = user.get_profile()
            profile.website = cd['website']
            profile.twitter = cd['twitter']
            profile.github = cd['github']
            profile.gravatar = gravatar
            user.save()
            profile.save()
            return render_to_response("accounts/profile.html", 
                {"form": form, "message": u'Updated success', "gravatar":gravatar}, 
                context_instance=RequestContext(request))
        else:
            return render_to_response("accounts/profile.html", {"form": form}, 
                context_instance=RequestContext(request))
    else:
        gravatar = "http://www.gravatar.com/avatar/"+hashlib.md5(user.email.lower()).hexdigest()+"?"
        gravatar += urllib.urlencode({'d': default, 's':str(40)})
        user.profile.gravatar = gravatar
        user.profile.save()
        form = UserProfileForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'website': user.profile.website,
            'twitter': user.profile.twitter,
            'github': user.profile.github})
        return render_to_response("accounts/profile.html", {"form": form}, 
                context_instance=RequestContext(request)) 


def dashboard(request):
    """Home view,"""
    return render_to_response('dashboard.html',RequestContext(request))

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
                return HttpResponseRedirect("/accounts/profile/")
            else:
                return HttpResponseRedirect("/accounts/signup/")
    else:
        form = SignUpForm()
    return render_to_response('accounts/signup.html', {
        'form': form
    }, context_instance=RequestContext(request))

def signout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

def about(request):
    """ About page view """
    return render_to_response('about.html', context_instance=RequestContext(request))
