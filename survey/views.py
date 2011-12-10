from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from survey.models import *

def home(request):
    """Home View, displays public surveys if user not logged in,
    otherwise display public and private surveys"""
    user = request.user
    public_surveys = Survey.objects.filter(visibility='public')
    if user.is_authenticated:
        user_surveys = Survey.objects.filter(user__username=user.username)
        return render_to_response('survey/home.html', 
            {"user_surveys": user_surveys,
             "public_surveys": public_surveys},
            context_instance=RequestContext(request))
    return render_to_response('survey/home.html', 
        {"public_surveys": public_survey},
        context_instance=RequestContext(request))