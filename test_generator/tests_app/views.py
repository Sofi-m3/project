from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.db.models import Count
from .models import Test, Question, Answer, Result
from .forms import TestForm, QuestionForm, AnswerForm, TestSelectForm, UserNameForm

class TestListView(ListView):
    model = Test
    template_name = 'tests_app/test_list.html'
    context_object_name = 'tests'

    def get_queryset(self):
        return Test.objects.annotate(question_count=Count('question'))

class TestCreateView(View):
    template_name = 'tests_app/test_create.html'

    def get(self, request):
        test_form = TestForm()
        question_form = QuestionForm()
        answer_form = AnswerForm()
        return render(request, self.template_name, {
            'test_form': test_form,
            'question_form': question_form,
            'answer_form': answer_form,
        })

    def post(self, request):
        test_form = TestForm(request.POST)
        if test_form.is_valid():
            test = test_form.save()
            messages.success(request, f"Тест '{test.name}' успешно создан!")
            return redirect('test_edit', test_id=test.id)
        return render(request, self.template_name, {'test_form': test_form})

class TestEditView(View):
    template_name = 'tests_app/test_edit.html'

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        test_form = TestForm(instance=test)
        question_form = QuestionForm()
        answer_form = AnswerForm()
        return render(request, self.template_name, {
            'test': test,
            'test_form': test_form,
            'question_form': question_form,
            'answer_form': answer_form,
        })

    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        test_form = TestForm(request.POST, instance=test)
        if test_form.is_valid():
            test_form.save()
            messages.success(request, f"Тест '{test.name}' успешно обновлен!")
            return redirect('test_edit', test_id=test.id)
        return render(request, self.template_name, {
            'test': test,
            'test_form': test_form,
        })

class TestDeleteView(View):
    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        test_name = test.name
        test.delete()
        messages.success(request, f"Тест '{test_name}' успешно удален!")
        return redirect('test_list')

class QuestionAddView(View):
    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.test = test
            question.save()
            messages.success(request, "Вопрос успешно добавлен!")
        return redirect('test_edit', test_id=test.id)

class AnswerAddView(View):
    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.save()
            messages.success(request, "Ответ успешно добавлен!")
        return redirect('test_edit', test_id=question.test.id)

class TestTakeView(View):
    template_name = 'tests_app/test_take.html'

    def get(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        questions = test.question_set.all()

        if not questions.exists():
            messages.warning(request, "В этом тесте нет вопросов!")
            return redirect('test_list')

        user_form = UserNameForm()
        return render(request, self.template_name, {
            'test': test,
            'questions': questions,
            'user_form': user_form,
        })

    def post(self, request, test_id):
        test = get_object_or_404(Test, id=test_id)
        questions = test.question_set.all()
        total_questions = questions.count()
        score = 0

        user_form = UserNameForm(request.POST)
        if not user_form.is_valid():
            return render(request, self.template_name, {
                'test': test,
                'questions': questions,
                'user_form': user_form,
            })

        user_name = user_form.cleaned_data['user_name']

        for question in questions:
            answer_id = request.POST.get(f'question_{question.id}')
            if answer_id:
                answer = get_object_or_404(Answer, id=answer_id)
                if answer.is_correct:
                    score += 1

        Result.objects.create(
            test=test,
            user_name=user_name,
            score=score,
            total_questions=total_questions
        )

        messages.success(request, f"Тест завершен! Ваш результат: {score} из {total_questions}")
        return redirect('test_results', test_id=test.id)

class TestResultsView(ListView):
    template_name = 'tests_app/test_results.html'
    context_object_name = 'results'

    def get_queryset(self):
        self.test = get_object_or_404(Test, id=self.kwargs['test_id'])
        return Result.objects.filter(test=self.test).order_by('-date_taken')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['test'] = self.test
        return context

class AllResultsView(ListView):
    template_name = 'tests_app/all_results.html'
    context_object_name = 'results'
    queryset = Result.objects.select_related('test').order_by('-date_taken')

class TestSelectView(View):
    template_name = 'tests_app/test_select.html'

    def get(self, request):
        form = TestSelectForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TestSelectForm(request.POST)
        if form.is_valid():
            test = form.cleaned_data['test']
            return redirect('test_take', test_id=test.id)
        return render(request, self.template_name, {'form': form})