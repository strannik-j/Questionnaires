from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Questionnaire(models.Model):
    name = models.CharField(max_length=150, unique=True)
    start_date = models.DateField()
    stop_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    # question = models.ForeignKey('Question', related_name='questionnaires', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    TYPES = (
        (1, 'Ответ текстом'),
        (2, 'Ответ с выбором одного варианта'),
        (3, 'Ответ с выбором нескольких вариантов'),
    )
    text = models.TextField()
    type = models.IntegerField(choices=TYPES)
    questionnaire = models.ForeignKey('Questionnaire', related_name='questions', on_delete=models.CASCADE)
    # answer = models.ForeignKey('Answer', related_name='questions', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey('Question', related_name='answers', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text

class Result(models.Model):
    # user = models.ForeignKey(User, related_name='results', on_delete=models.CASCADE, null=True)
    user_uniq_id = models.IntegerField(null=True, blank=True)
    questionnaire = models.ForeignKey('Questionnaire', related_name='results', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', related_name='results', on_delete=models.CASCADE, null=True)
    answer = models.ForeignKey('Answer', related_name='answers', on_delete=models.CASCADE, null=True)
    answer_user_text = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.user_uniq_id}_{self.questionnaire}'

    class Meta:
        unique_together = ("question", "user_uniq_id")

