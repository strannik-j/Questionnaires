# Questionnaires

## Системные требования:
- Linux
- python 3.6 и выше
- Django 2.2.10
- Django REST framework

## Инструкция по установке:
1. Создаём каталоги для программы и виртуального окружения:
    sudo mkdir {/opt/questionnaires,/opt/env/questionnaires} -p

2. Меняем владельца каталогов на текущего пользователя:
    sudo chown -R $USER:$USER {/opt/questionnaires,/opt/env/questionnaires}

3. Создаём виртуальное окружение:
   python3 -m venv /opt/env/questionnaires

4. Активируем виртуальное окружение:
    sudo -u test source /opt/env/questionnaires/bin/activate
    
5. Загружаем свежую версию программы:
    cd /opt/questionnaires
    git clone https://github.com/strannik-j/Questionnaires.git .
    
6. Устанавливаем зависимости:
    pip install -r requirements.txt
    
7. Переходим во внутренний каталог:
    cd test_django
    
8. Создаём SECRET_KEY:
    pwgen -1 50
    
    Полученное значение копируем в файл test_django/settings.py
    вместо строки your_secret_key
   
9. Активируем базу данных:
    python3 manage.py migrate 

10. Создаём учётную запись администратора:
     python manage.py createsuperuser

11. Запускаем приложение:    
     python3 manage.py runserver
    
    
## Работа с API
API доступно по адресу: 127.0.0.1:8000/api/

Для работы от учетной записи администратора необходимо получить Token:
  python3 manage.py shell
  >>> from django.contrib.auth.models import User
  >>> from rest_framework.authtoken.models import Token
  >>> user = User.objects.get(pk=user_name)
  >>> Token.objects.create(user=user)
Вместо user_name подставьте имя пользователя администратора

###Общие термины:
 - questionnaires - опросы
 - questions - вопросы
 - answers - варианты ответов
 - answer_user_text - ответ пользователя текстом
 - results - результаты опросов
 - start_date - дата начала опроса
 - stop_date - дата окончания опроса
 - user_uniq_id - уникальны ID всех пользователей (в т.ч. анонимных)
 
###Методы:
#### GET:
- questionnaires/ - возвращает JSON с опросами, вопросами и вариантами ответов:
  curl -X GET http://127.0.0.1:8000/api/questionnaires/
  
  {questionnaires: [{
        id,
        questions:[{
            id,
            answer:[{
                id,
                text,
                question_id
                },]
            text,
            type,
            questionnaire_id,
           },]
        name,
        start_date,
        stop_date
        },]
   }

- questions/ - возвращает JSON с вопросами и вариантами ответов:
  curl -X GET http://127.0.0.1:8000/api/questions/
  
     {questions:[{
        id,
        answer:[{
          id,
          text,
          question_id
          },]
        text,
        type,
        questionnaire_id,
       },]
     } 
  
- answers/ - возвращает JSON с вариантами ответов:
  curl -X GET http://127.0.0.1:8000/api/answers/

     {answers:[{
        id,
        text,
        question_id
        },]
      }
      
- results/X - возвращает JSON с ответами пользователя, уникальный ID которого равен Х:
    curl -X GET http://127.0.0.1:8000/api/results/1
    
    {results:[{
        id,
        user_uniq_id,
        questionnaire_id,
        question_id,
        answer_id,
        answer_user_text
        },]
     }
 
 ###POST
- questionnaires/ - создаёт опросы:
  curl -X POST -d '{"questionnaire":{"name":"Первый опрос","start_date":"2020-8-12","stop_date":"2020-10-1"}}' http://127.0.0.1:8000/api/questionnaires/ -H 'Authorization: Token значение_токена' -H 'Content-Type: application/json'
  После создания опроса start_date невозможно изменить через API.

- questions/ - создаёт вопросы:
  curl -X POST -d '{"question":{"text":"Твой любимый цвет?","questionnaire_id":"1","type":"1"}}' http://127.0.0.1:8000/api/questions/ -H 'Authorization: Token значение_токена' -H 'Content-Type: application/json'
  типы вопросов:
  1 - ответ текстом
  2 - ответ с выбором одного варианта
  3 - ответ с выбором нескольких вариантов

- answers/ - создаёт варианты ответов:
  curl -X POST -d '{"answer":{"text":"Белый","question_id":"1"}}' http://127.0.0.1:8000/api/answers/ -H 'Authorization: Token значение_токена' -H 'Content-Type: application/json'

- results/ - добавляет ответы пользователей:
  curl -X POST -d '{"result":{"user_uniq_id":"5","questionnaire_id":"1", "question_id":"2","answer_id":"2", "answer_user_text":nul}}' http://127.0.0.1:8000/api/results/5 -H 'Content-Type: application/json'
  Если ответ содержит вариант - заполняется answer_id, если же текст в свободной форме - заполняется answer_user_text.

