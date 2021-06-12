from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from askcrowd.models import Question, Answer, Comment, Upvote, Downvote
from django.core.paginator import Paginator
from django.http import JsonResponse
from askcrowd.forms import AnswerForm, QuestionForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db.models import Count
# Create your views here.
@login_required
def home(request):
    if 'queryhtml' in request.GET:
     search_result = request.GET['queryhtml']
     quest = Question.objects.filter(title__icontains= search_result).order_by('-id')


    else:
      quest = Question.objects.annotate(total_comments=Count('answer__comment')).all().order_by('-id')
    pagenator = Paginator(quest, 5)
    page_num = request.GET.get('page', 1)
    quest = pagenator.page(page_num)
    params = {'quest': quest}
    return render(request, 'home.html', params)
@login_required
def ask_form(request):
    form= QuestionForm
    if request.method=='POST':
        questForm = QuestionForm(request.POST, request.FILES)
        if questForm.is_valid():
            questForm = questForm.save(commit=False)
            questForm.user = request.user
            questForm.save()
            messages.success(request, 'Question Has been Added')
            return HttpResponseRedirect('#')

    return render(request, 'ask-question.html',{'form':form})
@login_required
def detail(request, id):

    quests = Question.objects.get(pk = id)
    tags = quests.tags.split(',')
    answers = Answer.objects.filter(question = quests)
    answerform = AnswerForm
    if request.method == 'POST':
        answerdata = answerform(request.POST)
        if answerdata.is_valid():
            answer = answerdata.save(commit=False)
            answer.question = quests
            answer.user = request.user
            answer.save()
            messages.success(request, 'Answer has been submitted.')
            return HttpResponseRedirect('#')

    return render(request, 'detail.html',
                  {'quests': quests,
                  'tags': tags,
                  'answers': answers,
                  'answerform': answerform,
                   })
@login_required
# Question according to tag
def tag(request,tag):
    quest=Question.objects.annotate(total_comments=Count('answer__comment')).filter(tags__icontains=tag).order_by('-id')
    pagenator = Paginator(quest, 2)
    page_num = request.GET.get('page', 1)
    quest = pagenator.page(page_num)
    params = {'quest': quest, 'tag': tag }
    return render(request, 'tags.html', params)
@login_required
def save_comment(request):
    if request.method=='POST':
        comment = request.POST['comment']
        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        Comment.objects.create(
            answer = answer,
            comment = comment,
            user = user
        )
        return JsonResponse({'bool':True})
@login_required
def save_upvote(request):
    if request.method=='POST':
        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        check = Upvote.objects.filter(answer = answer, user = user).count()
        if check > 0:
            Upvote.objects.filter(answer=answer, user=user).delete()
            return JsonResponse({'bool': False})

        else:
           Upvote.objects.create(
            answer = answer,
            user = user
            )
           Downvote.objects.filter(answer=answer, user=user).delete()
           return JsonResponse({'bool':True})


@login_required
def save_downvote(request):
    if request.method=='POST':
        answerid = request.POST['answerid']
        answer = Answer.objects.get(pk=answerid)
        user = request.user
        check = Downvote.objects.filter(answer = answer, user = user).count()
        if check > 0:
            Downvote.objects.filter(answer=answer, user=user).delete()
            return JsonResponse({'bool': False})
        else:
           Downvote.objects.create(
            answer = answer,
            user = user
            )
           Upvote.objects.filter(answer=answer, user=user).delete()
           return JsonResponse({'bool':True})

def Update_Answer(request, id):
    ans = Answer.objects.get(pk=id)
    answerform = AnswerForm(request.POST or None,instance=ans)
    if answerform.is_valid():
         answerform.save()
         messages.success(request, 'Answer has been submitted.')
         return redirect('detail', ans.question.id)



    return render(request, 'update_answer.html',
                  {
                   'form': answerform
                   })

def Del_Answer(request, id):
    answers = Answer.objects.get(pk=id)
    answers.delete()
    return redirect('detail', answers.question.id)


def update_question(request, id):
    question = Question.objects.get(pk=id)
    question_form = QuestionForm(request.POST or None, instance=question)
    if question_form.is_valid():

        question_form.save()
        messages.success(request,'Question has been submitted')
        return HttpResponseRedirect('/askcrowd/ask')

    return render(request,'ask-question.html',
                  {
                      'form':question_form
                  })
def del_question(request, id):
    question = Question.objects.get(pk =id)
    question.delete()
    return HttpResponseRedirect('/askcrowd/ask')
