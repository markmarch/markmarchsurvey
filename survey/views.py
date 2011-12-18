from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render_to_response, get_object_or_404
from survey.models import *
from survey.forms import *
from datetime import datetime, time

def home(request):
    """Home View, displays public surveys if user not logged in,
    otherwise display public and private surveys"""
    user = request.user
    public_surveys = Survey.objects.filter(visibility='public')
    if user.is_authenticated:
        user_surveys = Survey.objects.filter(user__username=user.username)[:6]
        return render_to_response('survey/home.html', 
            {"user_surveys": user_surveys,
             "public_surveys": public_surveys},
            context_instance=RequestContext(request))
    return render_to_response('survey/home.html', 
        {"public_surveys": public_survey},
        context_instance=RequestContext(request))
        
def survey(request, survey_id):
    """Survey view, list survey details"""
    survey = Survey.objects.get(pk=survey_id)
    if survey is not None:
        user = request.user
        editable = survey.belongs_to(user)
        return render_to_response('survey/survey.html', {'survey': survey, 'editable': editable},
            context_instance=RequestContext(request))
    else:
        return render_to_response('404.html', {'error': ['Survey not found']},
            context_instance=RequestContext(request))
 
@login_required(login_url='/accounts/signin/')
def new(request):
    """Create new survey"""
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            survey = Survey(user=user, name=cd['name'], desc=cd['desc'],
                visibility=cd['visibility'])
            if cd['expires'] and cd['expire_date'] is not None:
                survey.expire_date = datetime.combine(cd['expire_date'], time())
            survey.save()
            form = PollForm()
            messages.success(request, 'Survey Created')
            return render_to_response('survey/add_question.html', 
                {'survey': survey, 'form': form},
                context_instance=RequestContext(request))
        else:
            messages.error(request, "Can't create survey.")
            return render_to_response('survey/new.html', {"form": form},
                context_instance=RequestContext(request))
    else:
        return render_to_response('survey/new.html', {"form": SurveyForm()},
            context_instance=RequestContext(request))

                   
@login_required(login_url='/accounts/signin/')
def add(request, survey_id):
    """Add a new question to survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    user = request.user
    if request.method != 'POST':
        return HttpResponseRedirect('/home/')
    
    if survey.belongs_to(user):
        form = PollForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            question=cd['question']
            poll = Poll(survey=survey, question=question)
            poll.save()
            for k in request.POST.keys():
                if k.startswith('option_'):
                    choice = request.POST.get(k)
                    if choice != "":
                        c = Choice(poll=poll, choice=choice)
                        c.save()
            messages.success(request, 'Question Added')
            return render_to_response(
                'survey/add_question.html',
                {'survey': survey, 'form': PollForm()},
                context_instance=RequestContext(request))
        else:
            messages.error(request, 'Failed to add question')
            return render_to_response('survey/add_question.html',
                {'survey': survey, 'form': form},
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/survey/' + str(survey.pk) + '/')

    
              
@login_required(login_url='/accounts/signin/')
def vote(request, survey_id):
    """Vote on a survey"""
    survey = Survey.objects.get(pk=survey_id)
    user = request.user
    if request.method != 'POST':
        return render_to_response('survey/survey.html', {'survey': survey},
            context_intance=RequestContext(request))
    
    if survey is not None and survey.can_vote(user):

        return render_to_response('survey/results.html', {'survey': survey},
            context_instance=RequestContext(request))
    else:
        return render_to_response('survey/survey.html', {'survey': survey},
            context_instance=RequestContext(request))
        
        