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
    survey = get_object_or_404(Survey, pk=survey_id)
    user = request.user
    editable = survey.belongs_to(user)
    return render_to_response('survey/survey.html', 
        {'survey': survey, 'editable': editable},
        context_instance=RequestContext(request))
 
@login_required(login_url='/accounts/signin')
def edit(request, survey_id):
    """Edit a survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.belongs_to(request.user) is False:
        messages.error(request, 'You can not eidt this survey')
        return render_to_response('survey/survey.html',
            {'survey': survey, 'editable': False},
            context_instance=RequestContext(request))
    expires = survey.expire_date is not None
    month, day, year = 0, 0, 0
    if expires:
        month = survey.expire_date.month
        day = survey.expire_date.day
        year = survey.expire_date.year
    if request.method == 'GET':
        return render_to_response('survey/new.html', 
            {
            'name': survey.name,
            'desc': survey.desc,
            'expires': expires,
            'month': month,
            'day': day,
            'year': year,
            'visibility': survey.visibility,
            'edit': True,
            'survey_id': survey_id
            },
            context_instance=RequestContext(request))
    else:
        if request.method == 'POST':
            form = SurveyForm(request.POST)
            if form.is_valid():
                cd = form.cleaned_data
                survey.name = cd['name']
                survey.desc = cd['desc']
                if cd['expires']:
                    survey.expire_date = cd['expire_date']
                survey.visibility = cd['visibility']
                survey.save()
                messages.success(request, 'Update sucess')
                return HttpResponseRedirect('/survey/' + survey_id + '/question/edit')
            else:
                for k, v in form.errors.items():
                    messages.error(request, v[0])
                return render_to_response('survey/new.html', 
                    {
                        'name': survey.name,
                        'desc': survey.desc,
                        'expires': expires,
                        'month': month,
                        'day': day,
                        'year': year,
                        'visibility': survey.visibility,
                        'edit': True,
                        'survey_id': survey_id
                    },
                    context_instance=RequestContext(request))
        else:
            raise Http404

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
def add_question(request, survey_id):
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
def edit_question(request, survey_id):
    """Edit questions in a survey"""
    return HttpResponseRedirect('/home/')

@login_required(login_url='/accounts/signin/')
def comment(request, survey_id):
    """Comment on a survey"""
    user = request.user
    survey = get_object_or_404(Survey, pk=survey_id)
    if request.method != 'POST':
        return HttpResponseRedirect('/survey/' + survey_id + '/')
    form = CommentForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        comment = Comment(survey=survey, user=user, comment=cd['comment'])
        comment.save()
        messages.success(request, "Comment Success")
        return HttpResponseRedirect('/survey/'+survey_id + '/')
    else:
        messages.error(request, "Comment failed")
        return HttpResponseRedirect('/survey/'+survey_id + '/')

    
              
@login_required(login_url='/accounts/signin/')
def vote(request, survey_id):
    """Vote on a survey"""
    survey = Survey.objects.get(pk=survey_id)
    user = request.user
    if request.method != 'POST':
        return render_to_response('survey/survey.html', {'survey': survey},
            context_intance=RequestContext(request))
    
    if survey is not None and survey.can_vote(user):
        polls = Poll.objects.filter(survey__pk=survey_id)
        for p in polls:
            choice = Choice.objects.get(pk=request.POST[str(p.pk)])
            p.vote(user,choice)
        return HttpResponseRedirect('/survey/' + str(survey_id) + '/')
    else:
        return render_to_response('survey/survey.html', {'survey': survey},
            context_instance=RequestContext(request))
        
        