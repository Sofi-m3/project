from django import forms
from .models import Test, Question, Answer, Result

class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']
        widgets = {
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer_text', 'is_correct']
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_correct': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TestSelectForm(forms.Form):
    test = forms.ModelChoiceField(
        queryset=Test.objects.all(),
        label="Выберите тест",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

class UserNameForm(forms.Form):
    user_name = forms.CharField(
        max_length=100,
        label="Ваше имя",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )