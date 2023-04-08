from django.urls import path
from . import views
from .views import QuizListCreateView, QuizRetrieveUpdateDestroyView

urlpatterns = [
    path("", views.home, name = "home"),
    path("signup/", views.register, name="signup"),
    path('form-submission/', views.save_quiz_data, name='save_quiz_data'),
    path("questions/", views.questions_page, name='questions_page'),
    path('questions/questions_list/', QuizListCreateView.as_view()),
    path('questions/questions_list/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view()),
    path('load-questions/', views.load_questions, name='load-questions'),
    path('get-question/<int:question_id>/', views.get_question, name='get-question'),
    path('save-question/', views.save_question, name='save-question'),
    path('delete-question/<int:question_id>/', views.delete_question, name='delete-question'),
]
