from django.db import models
from django.utils import timezone
class Test(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название теста")
    description = models.TextField(blank=True, null=True, verbose_name="Описание теста")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    question_text = models.TextField(verbose_name="Текст вопроса")

    def __str__(self):
        return f"{self.test.name} - {self.question_text[:50]}..."

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name="Вопрос")
    answer_text = models.TextField(verbose_name="Текст ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильный ответ")

    def __str__(self):
        return f"{self.question.question_text[:30]}... - {self.answer_text[:30]}..."

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name="Тест")
    user_name = models.CharField(max_length=100, verbose_name="Имя пользователя")
    score = models.IntegerField(verbose_name="Баллы")
    total_questions = models.IntegerField(verbose_name="Всего вопросов")
    date_taken = models.DateTimeField(default=timezone.now, verbose_name="Дата прохождения")

    def __str__(self):
        return f"{self.user_name} - {self.test.name} - {self.score}/{self.total_questions}"

    class Meta:
        verbose_name = "Результат"
        verbose_name_plural = "Результаты"
        ordering = ['-date_taken']