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
        return render_to_response('survey/edit.html', 
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
                if cd['expires'] is False and survey.expire_date is not None:
                    survey.expire_date = None
                
                survey.visibility = cd['visibility']
                survey.save()
                messages.success(request, 'Update sucess')
                return HttpResponseRedirect('/survey/' + survey_id + '/question/edit')
            else:
                for k, v in form.errors.items():
                    messages.error(request, v[0])
                return render_to_response('survey/edit.html', 
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
            return render_to_response('survey/edit.html', {"form": form},
                context_instance=RequestContext(request))
    else:
        return render_to_response('survey/edit.html', {"form": SurveyForm()},
            context_instance=RequestContext(request))

                   
@login_required(login_url='/accounts/signin/')
def add_question(request, survey_id):
    """Add a new question to survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    user = request.user
    if request.method == 'GET':
        return render_to_response(
                'survey/add_question.html',
                {'survey': survey, 'form': PollForm()},
                context_instance=RequestContext(request))
    if request.method != 'POST':
        raise Http404

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
def edit_survey_questions(request, survey_id):
    """Edit questions in a survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    user = request.user
    if survey.belongs_to(user):
        return render_to_response('survey/edit_question.html', 
            {'survey': survey},
            context_instance=RequestContext(request))
    else:
        messages.error(request, 'Computer say no, because this is not yours')
        return HttpResponseRedirect('/survey/' + survey_id + '/') 


@login_required(login_url='/accounts/signin/')
def delete_question(request, survey_id, question_id):
    """Delete a question"""
    survey = get_object_or_404(Survey, pk=survey_id)
    user = request.user
    if survey.belongs_to(user):
        poll = get_object_or_404(Poll, pk=question_id)
        poll.delete()
        messages.success(request, 'Question deleted')
        return HttpResponseRedirect('/survey/' + survey_id + '/question/edit/');
    else:
        messages.error(request, 'Computer say no, because this is not yours')
        return HttpResponseRedirect('/survey/' + survey_id + '/') 

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
def edit_question(request, survey_id, poll_id):
    """Edit a quesiton in given poll"""
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.belongs_to(request.user) is False:
        messages.error(request, 'Computer say no, because this is not yours')
        return HttpResponseRedirect('/survey/' + survey_id + '/') 
    
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.method != 'POST':
        return HttpResponseRedirect('/survey/' + survey_id + '/') 

    form = PollForm(request.POST)
    if form.is_valid():
        cd = request.POST
        for c in poll.choices():
            if cd['option_' + str(c.pk)] != '':
                c.choice = cd['option_' + str(c.pk)]
                c.save()
            else:
                c.delete()
        for k,v in cd.items():
            if k.startswith('newoption_'):
                choice = Choice(poll=poll,choice=cd[k])
                choice.save()
        messages.success(request, 'Question updated')
        return HttpResponseRedirect('/survey/' + survey_id + '/question/edit/');
    else:
        for k, v in form.errors.items():
            messages.error(request, v[0])
        return HttpResponseRedirect('/survey/' + survey_id + '/question/edit/');    
        


@login_required(login_url='/accounts/signin/')
def delete(request, survey_id):
    """Delete a survey"""
    user = request.user
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.belongs_to(user):
        survey.delete()
        messages.success(request, 'Survey deleted')
        return HttpResponseRedirect('/home/')
    else:
        messages.error(request, 'Computer say no, because this is not yours')
        return HttpResponseRedirect('/survey/' + survey_id + '/') 
              
@login_required(login_url='/accounts/signin/')
def vote(request, survey_id):
    """Vote on a survey"""
    survey = get_object_or_404(Survey, pk=survey_id)
    if survey.is_expired:
        messages.error(request, 'This survey is expired')
        return HttpResponseRedirect('/survey/' + survey_id + '/')
    
    user = request.user
    if request.method != 'POST':
        return render_to_response('survey/survey.html', {'survey': survey},
            context_intance=RequestContext(request))
    
    if survey is not None and survey.can_vote(user):
        for k, v in request.POST.items():
            if k.startswith('poll_'):
                poll = Poll.objects.get(pk=k[5:])
                poll.vote(user, Choice.objects.get(pk=v))
        return HttpResponseRedirect('/survey/' + str(survey_id) + '/')
    else:
        return render_to_response('survey/survey.html', {'survey': survey},
            context_instance=RequestContext(request))
        
        