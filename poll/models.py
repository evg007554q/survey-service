from django.db import models

from config import settings


# Create your models here.
class Survey(models.Model):
    """ Опрос """
    name = models.CharField(max_length=100, verbose_name='наименование опроса')
    description = models.CharField(max_length=250, verbose_name='описание опроса', null=True, blank=True)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                              verbose_name='Создатель')

    def __str__(self):
        return f'{self.name} '

    class Meta:
        verbose_name = 'опрос'
        verbose_name_plural = 'опросы'
        ordering = ('name',)


class Question(models.Model):
    """ Вопросы опроса"""
    name = models.CharField(max_length=100, verbose_name='наименование вопроса')
    survey = models.ForeignKey('Survey', on_delete=models.CASCADE, verbose_name='опрос')
    first = models.BooleanField(verbose_name='первый', null=True, blank=True)


    def __str__(self):
        return f'{self.name} -({self.survey.name})'

    class Meta:
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
        ordering = ('name',)


class Possible_answer(models.Model):
    """ Вариант ответа на вопрос"""
    name = models.CharField(max_length=100, verbose_name='Ответ')

    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='вопрос')
    next_question = models.ForeignKey('Question', related_name='next_question', on_delete=models.SET_NULL,
                                      null=True, blank=True, verbose_name='следующий вопрос')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Вариант ответа '
        verbose_name_plural = 'Вариант ответов '
        ordering = ('name',)


class User_answer(models.Model):
    """ Ответ пользователя """
    question = models.ForeignKey('Question', on_delete=models.CASCADE, verbose_name='вопрос')
    answer = models.ForeignKey('Possible_answer', on_delete=models.CASCADE, verbose_name='категория')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='пользователь')

    def __str__(self):
        return f'{self.answer.name} - {self.user.name}'

    class Meta:
        verbose_name = 'ответ пользователя '
        verbose_name_plural = 'ответы пользователя '
        ordering = ('question',)
