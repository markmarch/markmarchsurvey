from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response

def home(request):
    """Home View, displays public surveys if user not logged in,
    otherwise display public and private surveys"""
    return render_to_response('survey/home.html', context_instance=RequestContext(request))