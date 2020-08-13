from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Question, Questionnaire, Answer, Result
from django.contrib.auth.models import User



class AnswerSerializer(serializers.Serializer):
    id =  serializers.IntegerField(required=False)
    text = serializers.CharField(max_length=255)
    question_id = serializers.IntegerField()

    def create(self, validated_data):
        return Answer.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.question_id = validated_data.get('question_id', instance.question_id)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance


class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    answers = AnswerSerializer(many=True, read_only=True, required=False)
    text = serializers.CharField()
    type = serializers.IntegerField()
    questionnaire_id = serializers.IntegerField()

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.questionnaire_id = validated_data.get('questionnaire_id', instance.questionnaire_id)
        instance.text = validated_data.get('text', instance.text)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


class QuestionnaireSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    questions = QuestionSerializer(many=True, read_only=True, required=False)
    name = serializers.CharField(max_length=150)
    start_date = serializers.DateField()
    stop_date = serializers.DateField()
    description = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return Questionnaire.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        # instance.start_date = validated_data.get('start_date', instance.start_date)  # Запрет на изменение start_date
        instance.stop_date = validated_data.get('stop_date', instance.stop_date)
        instance.save()
        return instance


class ResultSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False)
    user_uniq_id = serializers.IntegerField()
    questionnaire_id = serializers.IntegerField()
    question_id = serializers.IntegerField()
    answer_id = serializers.IntegerField(required=False, allow_null=True)
    answer_user_text = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    def create(self, validated_data):
        return Result.objects.create(**validated_data)




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
