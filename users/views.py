from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from rest_framework import generics, status
from .models import Question, Quiz, Answer
from .serializers import QuestionSerializer, QuizSerializer
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import json


def home(request):
    return render(request, "users/home.html")


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/accounts/login/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def questions_page(request):
    return render(request, 'questions.html')


class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


@api_view(['POST'])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def questions_list(request):
    # Получение списка вопросов из базы данных или другого источника
    questions_list = Question.objects.all()
    context = {
        'questions_list': questions_list,
    }
    return render(request, 'questions_list.html', context)


def index(request):
    return render(request, 'questions_list.html')


def load_questions(request):
    questions = Question.objects.all().values('id', 'text')
    data = {'questions': list(questions)}
    return JsonResponse(data)


def get_question(request, question_id):
    question = Question.objects.get(id=question_id)
    data = {'question': question.text}
    return JsonResponse(data)


@csrf_exempt
def save_question(request):
    data = json.loads(request.body)
    question_text = data['question']
    question_id = data.get('id')
    if question_id:
        question = Question.objects.get(id=question_id)
        question.text = question_text
        question.save()
    else:
        question = Question.objects.create(text=question_text)
    data = {'id': question.id, 'question': question.text}
    return JsonResponse(data)


@csrf_exempt
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    question.delete()
    data = {'message': 'Question deleted successfully!'}
    return JsonResponse(data)


@api_view(['POST'])
def create_quiz(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        quiz = serializer.save()
        for question in quiz.questions.all():
            question_text = question.text
            for answer in question.answers.all():
                answer_text = answer.text
                if answer.is_correct:
                    question.correct_answer = answer
                    question.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def save_quiz_data(request):
    serializer = QuizSerializer(data=request.data)
    if serializer.is_valid():
        quiz_id = request.data.get('id')
        if quiz_id:
            quiz = Quiz.objects.get(id=quiz_id)
            serializer.update(quiz, serializer.validated_data)
        else:
            quiz = serializer.save()
        return Response(QuizSerializer(quiz).data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

@api_view(['POST'])
def check_answers(request, quiz_id):
    quiz = Quiz.objects.get(id=quiz_id)
    question_ids = request.data.keys()
    questions = quiz.questions.filter(id__in=question_ids)
    score = 0
    results = []
    for question in questions:
        correct_answers = question.answers.filter(is_correct=True)
        answered_ids = request.data[str(question.id)]
        answered = Answer.objects.filter(id__in=answered_ids)
        is_correct = set(answered) == set(correct_answers)
        if is_correct:
            score += 1
        results.append({'question': question.text, 'correct': is_correct})
    response_data = {'score': score, 'total': len(questions), 'results': results}
    return JsonResponse(response_data)