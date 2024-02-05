from django.contrib import admin

from poll.models import Survey, Question, Possible_answer


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_filter = ('owner',)
    search_fields = ('name', 'description')


@admin.register(Possible_answer)
class Possible_answerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'question', 'next_question')
    list_filter = ('question',)
    search_fields = ('name', 'description')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'survey')
    list_filter = ('survey',)
    search_fields = ('name', 'description')
    # list_select_related = ['Question']
    # inlines = [Possible_answerAdmin]

# admin.site.register(Question, Possible_answerAdmin)
