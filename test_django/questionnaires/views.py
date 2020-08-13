from django.contrib.auth import authenticate
# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.urls import reverse
from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date
from .models import Questionnaire, Question, Answer, Result
from .serializers import QuestionnaireSerializer, QuestionSerializer, AnswerSerializer, ResultSerializer, UserSerializer


class QuestionnaireView(APIView):
    def get(self, request):
        questionnaires = Questionnaire.objects.all()
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response({"questionnaires": serializer.data})

    def post(self, request):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        questionnaire = request.data.get("questionnaire")
        serializer = QuestionnaireSerializer(data=questionnaire)
        if serializer.is_valid(raise_exception=True):
            questionnaire_saved = serializer.save()
        return Response({"success": "Questionnaire '{}' created successfully".format(questionnaire_saved.name)})

    def put(self, request, pk):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        saved_questionnaire = get_object_or_404(Questionnaire.objects.all(), pk=pk)
        data = request.data.get('questionnaire')
        serializer = QuestionnaireSerializer(instance=saved_questionnaire, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            questionnaire_saved = serializer.save()
        return Response({
            "success": "Questionnaire '{}' updated successfully".format(questionnaire_saved.name)
        })


class ActiveQuestionnaireView(APIView):
    def get(self, request):
        questionnaires = Questionnaire.objects.filter(
            start_date__lte=date.today(),
            stop_date__gte=date.today(),
        )
        serializer = QuestionnaireSerializer(questionnaires, many=True)
        return Response({"questionnaires": serializer.data})


class ResultView(APIView):
    def get(self, request, uniq_id=None):
        results = None
        if uniq_id:
            results = Result.objects.filter(
                user_uniq_id = uniq_id
            )

        elif request.user.username == 'admin':
            results = Result.objects.all()
        serializer = ResultSerializer(results, many=True)
        return Response({'results': serializer.data})

    def post(self, request, uniq_id=None):
        result = request.data.get("result")
        serializer = ResultSerializer(data=result)
        if serializer.is_valid(raise_exception=True):
            result_saved = serializer.save()
        return Response({"success": "Result '{}' created successfully".format(result_saved)})


@permission_classes((AllowAny,))
class QuestionView(APIView):
    def get(self, request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions, many=True)
        return Response({"questions": serializer.data})

    def post(self, request):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        question = request.data.get("question")
        serializer = QuestionSerializer(data=question)
        if serializer.is_valid(raise_exception=True):
            question_saved = serializer.save()
        return Response({"success": "Question '{}' created successfully".format(question_saved.text)})

    def put(self, request, pk):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        saved_question = get_object_or_404(Question.objects.all(), pk=pk)
        data = request.data.get('question')
        serializer = QuestionSerializer(instance=saved_question, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            question_saved = serializer.save()
        return Response({
            "success": "Question '{}' updated successfully".format(question_saved.text)
        })


class AnswerView(APIView):
    def get(self, request):
        answers = Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response({"answers": serializer.data})

    def post(self, request):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        answer = request.data.get("answer")
        serializer = AnswerSerializer(data=answer)
        if serializer.is_valid(raise_exception=True):
            answer_saved = serializer.save()
        return Response({"success": "Answer '{}' created successfully".format(answer_saved.text)})

    def put(self, request, pk):
        if request.user.username != 'admin':
            return Response({'error': 'Access denied'})
        saved_answer = get_object_or_404(Answer.objects.all(), pk=pk)
        data = request.data.get('answer')
        serializer = AnswerSerializer(instance=saved_answer, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            answer_saved = serializer.save()
        return Response({
            "success": "Answer '{}' updated successfully".format(answer_saved.text)
        })


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer



class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)