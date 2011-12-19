from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.messages.api import get_messages
from django.core.context_processors import csrf
import urllib, hashlib
from django.contrib.auth.models import User

from forms import *
from survey.models import *
from models import *
from itertools import chain

def signin(request):
    """Login View"""
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    next = request.POST['next']
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponseRedirect("/")
            else:
                errors = form._errors.setdefault(forms.forms.NON_FIELD_ERRORS, forms.util.ErrorList())
                errors.append(u"Invalid username or password")
        return render_to_response('accounts/signin.html', {"form": form}, 
            context_instance=RequestContext(request))
    else:
        next = request.GET.get('next', '/')
        form = SignInForm()
        return render_to_response('accounts/signin.html', {"form": form, "next": next},
            context_instance=RequestContext(request))

@login_required(login_url='/accounts/signin/')
def profile(request):
    """User Profile page"""
    user = request.user
    profile = user.profile
    default = "http://www.gravatar.com/avatar/"
    user_surveys = Survey.objects.filter(user=user)
    mutual = Friendship.objects.filter(status='mutual')
    friends = list(chain(mutual.filter(user_a=user).values('user_b'),
        mutual.filter(user_b=user).values('user_a')))
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
            messages.success(request, 'Update success')
            return render_to_response("accounts/profile.html", 
                {
                "form": form, 
                "surveys": user_surveys,
                "friends": friends
                }, 
                context_instance=RequestContext(request))
        else:
            return render_to_response("accounts/profile.html",
                {
                "form": form, 
                "surveys": user_surveys,
                "friends": friends
                },  
                context_instance=RequestContext(request))
    else:
        is_first = request.GET.get('first', False)
        if is_first:
            gravatar = "http://www.gravatar.com/avatar/"+hashlib.md5(user.email.lower()).hexdigest()+"?"
            gravatar += urllib.urlencode({'d': default, 's':str(40)})
            profile = user.get_profile()
            profile.gravatar = gravatar
            profile.save()
        form = UserProfileForm(initial={
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'website': user.profile.website,
            'twitter': user.profile.twitter,
            'github': user.profile.github})
        return render_to_response("accounts/profile.html", 
                {
                "form": form, 
                "surveys": user_surveys,
                "friends": friends
                }, 
                context_instance=RequestContext(request)) 

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
                return HttpResponseRedirect("/accounts/profile/?first=true")
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

def user(request, username):
    """User page view"""
    user = get_object_or_404(User, username=username)
    surveys = Survey.objects.filter(user=user)
    return render_to_response('accounts/user.html', {'u': user, 'surveys': surveys},
        context_instance=RequestContext(request))

def userlist(request):
    """User list page"""
    users = User.objects.all()
    return render_to_response('userlist.html', {'users': users},
        context_instance=RequestContext(request))