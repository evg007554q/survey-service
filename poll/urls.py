from django.urls import path

from poll.apps import PollConfig
from poll.views import index, start_poll, vote_poll, next_question

app_name = PollConfig.name


urlpatterns = [
    path('', index, name='index'),
    path('<int:pk>/start_poll', start_poll, name='start_poll'),
    path('<int:pk>/vote_poll', vote_poll, name='vote_poll'),
    path('<int:pk>/next_question', next_question, name='next_question'),
]