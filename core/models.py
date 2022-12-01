from django.db import models
from django.contrib.auth.models import User


class Tests(models.Model):
    title = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Тесты"
        verbose_name_plural = "Тесты"
        ordering = ["id"]


class Questions(models.Model):
    question_text = models.TextField()
    answer = models.CharField(max_length=30)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Вопросы"
        verbose_name_plural = "Вопросы"
        ordering = ["test"]


class Answers(models.Model):
    answers = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    test = models.ForeignKey(Tests, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Ответы пользователей"
        verbose_name_plural = "Ответы пользователей"
        ordering = ["id"]


class UserAdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField()
    finished_tests_count = models.IntegerField()

    class Meta:
        verbose_name = "Дополнительные поля пользователей"
        verbose_name_plural = "Дополнительные поля пользователей"
        ordering = ["balance"]
