from django.contrib import admin
from .models import Test, Question, Answer, Result

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1
    fields = ['answer_text', 'is_correct']

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ['question_text']
    show_change_link = True
    inlines = [AnswerInline]

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['test', 'question_text']
    list_filter = ['test']
    search_fields = ['question_text']
    inlines = [AnswerInline]

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer_text', 'is_correct']
    list_filter = ['question__test', 'is_correct']
    search_fields = ['answer_text']

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'test', 'score', 'total_questions', 'date_taken']
    list_filter = ['test', 'date_taken']
    search_fields = ['user_name']
    readonly_fields = ['date_taken']