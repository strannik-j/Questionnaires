from django.contrib import admin

# Register your models here.

from .models import Questionnaire, Question, Answer, Result
admin.site.register(Questionnaire)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Result)