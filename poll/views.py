from django.shortcuts import render
from poll.models import Survey, Possible_answer, Question, User_answer

from django.db import connection

def my_custom_sql(q_text, pk):
    with connection.cursor() as cursor:
        cursor.execute(q_text, [pk])
        # row = cursor..fetchone()
        rows = cursor.fetchall()
    return rows

# Create your views here.
def index(request):
    context = {
        'object_list': Survey.objects.all(),
        'title': 'Доступные опросы'
    }
    return render(request, 'poll/index.html', context)


def start_poll(request, pk):
    # Possible_answer
    # Question
    # pk - poll

    survey_p = Survey.objects.get(pk=pk)
    question_p = Question.objects.get(survey=survey_p.pk, first=True)
    possible_answer_list = Possible_answer.objects.filter(question=question_p.pk)


    context = {
        'object_list': possible_answer_list,
        'title': question_p.name,
        'Question_pk': question_p.pk
    }
    return render(request, 'poll/poll.html', context)

def vote_poll(request, pk):
    possible_answer_pk = request.POST.get("op")
    possible_answer_o = Possible_answer.objects.get(pk=possible_answer_pk)
    question_p = Question.objects.get(pk=pk)

    if possible_answer_pk:

        answer = User_answer.objects.create(question=question_p, answer=possible_answer_o, user=request.user)
        answer.save()


    title = f'Выбран вариант {possible_answer_o.name}'
    question = Question.objects.get(pk=pk).name
    q_text = '''SELECT count(users_user.id) as alluser, 
                (SELECT count(poll_user_answer.user_id) FROM poll_user_answer
                where poll_user_answer.question_id=%s)  as answeruser
                FROM users_user 
                '''
    meeting_list = my_custom_sql(q_text, pk)

    for ml in meeting_list:
        alluser = ml[0]
        answeruser= ml[1]
        title1 = f'Всего опрошено {round(100*answeruser/alluser,2)}% пользователей {answeruser}( из {alluser})'


    q_text = '''SELECT 
                RANK() OVER( ORDER BY count(poll_user_answer.id)  DESC) as ROW, 
                poll_possible_answer.name, count(poll_user_answer.id) as vote
                ,(SELECT count(poll_user_answer.id) from poll_user_answer 
                  where poll_user_answer.question_id=poll_possible_answer.question_id) as all_vote
	            FROM public.poll_possible_answer
            	left join poll_user_answer 
        	    	on poll_user_answer.answer_id=poll_possible_answer.id
            	where poll_possible_answer.question_id=%s
            	GROUP BY poll_possible_answer.name, poll_possible_answer.question_id'''

    user_answer_list = my_custom_sql(q_text, pk)
    object_list = []
    for ml in user_answer_list:
        title_l=f'{ml[0]}. {ml[1]} выбрали {ml[2]} ({round(100*ml[2]/ml[3],2)}%) '
        object_list.append(title_l)

    # object_list = Possible_answer.objects.raw(q_text, [pk])
    if possible_answer_o.next_question:
        context = {
            'object_list': object_list,
            'question': question,
            'title': title,
            'title1': title1,
            'next_question': possible_answer_o.next_question.pk
        }
    else:
        context = {
            'object_list': object_list,
            'question': question,
            'title': title,
            'title1': title1,
            'next_question': 0
        }

    return render(request, 'poll/result.html', context)

def next_question(request, pk):
    Question_p = Question.objects.get(pk=pk)
    Possible_answer_list = Possible_answer.objects.filter(question=pk)


    context = {
        'object_list': Possible_answer_list,
        'title': Question_p.name,
        'Question_pk': pk
    }
    return render(request, 'poll/poll.html', context)

