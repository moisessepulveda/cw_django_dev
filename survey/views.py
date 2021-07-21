from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from survey.models import Question, Answer
from django.db.models import Case, When, Value, F

from datetime import datetime
from datetime import date
class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        questions = get_question_ranking()
        return questions


def get_question_ranking():
    questions = Question.objects.annotate(
                ranking_calculated = Case(
                    When(created__year=date.today().year,
                                        created__month=date.today().month,
                                        created__day=date.today().day, then = F("ranking") + Value(10),
                                        )
                                        ,default=F("ranking")
                )
                
            ).order_by('-ranking_calculated')[:20]

    return questions

class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user

        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    question_pk = request.POST.get('question_pk')
    print(request.POST)
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.filter(question=question, author=request.user).first()
    if not answer:
        answer = Answer(author=request.user, question=question)
    answer.value = request.POST.get('value')
    answer.save()
    question.ranking = calculate_ranking(question)
    question.save()

    return JsonResponse({'ok': True})

def like_dislike_question(request):
    question_pk = request.POST.get('question_pk')
    if not request.POST.get('question_pk'):
        return JsonResponse({'ok': False})
    question = Question.objects.filter(pk=question_pk)[0]
    answer = Answer.objects.filter(question=question, author=request.user).first()
    if not answer:
        answer = Answer(author=request.user, question=question)
    
    answer.like = request.POST.get("like_value")
    answer.save()
    question.ranking = calculate_ranking(question)
    question.save()

    return JsonResponse({'ok': True})

def calculate_ranking(question):
    answers = question.answers.all()
    ranking = 0
    for a in answers:
        if a.like == 1:
            ranking += 5
        elif a.like == 2:
            ranking -= 3
        ranking += 10
    
    return ranking



def questions_template(request):
    data = {
        "object_list": get_question_ranking()
    }
    return render(request, "survey/question_list.html", data)