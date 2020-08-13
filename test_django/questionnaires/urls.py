from django.urls import path
from rest_framework import views

from .views import QuestionnaireView, QuestionView, AnswerView, ActiveQuestionnaireView, ResultView, UserCreate, LoginView

app_name = 'questionnaires'

urlpatterns = [
    path('questionnaires/', QuestionnaireView.as_view()),
    path('active_questionnaires/', ActiveQuestionnaireView.as_view()),
    path('questions/', QuestionView.as_view()),
    path('answers/', AnswerView.as_view()),
    path('results/', ResultView.as_view()),
    path('results/<int:uniq_id>', ResultView.as_view()),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    # path("login/", views.obtain_auth_token, name="login"),
]