import json
import logging
from django.http import (
    HttpResponseServerError, HttpResponseNotFound,
    HttpResponseRedirect, HttpResponse
)
from django.views import View
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterUserForm
from django.urls import reverse_lazy, reverse
from .models import Tests, Questions, Answers, UserAdditionalInfo
from django.contrib.auth.models import User
from django.shortcuts import render


logger = logging.getLogger("debug")


# Базовый класс для обработки непредвиденных ошибок
class BaseView(View):
    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except Exception as e:
            logger.error(e)
            return HttpResponseServerError(e)


class RegisterUser(BaseView, CreateView):
    form_class = RegisterUserForm
    template_name = "core/reg.html"
    success_url = reverse_lazy("index_page")

    def get(self, request, *args, **kwargs):
        if request.session.keys():
            return HttpResponseRedirect(reverse("index_page"))
        return super().get(request, *args, **kwargs)


class UserAuth(BaseView, LoginView):
    form_class = AuthenticationForm
    template_name = "core/auth.html"

    def get(self, request, *args, **kwargs):
        if request.session.keys():
            return HttpResponseRedirect(reverse("index_page"))
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("index_page")


class UserLogout(LogoutView):
    next_page = reverse_lazy("index_page")


class Index(BaseView, TemplateView):
    template_name = "core/index.html"
    user_id = int()

    def get(self, request, *args, **kwargs):
        if request.session.keys():
            self.user_id = request.session.get("_auth_user_id")

            user_additional = UserAdditionalInfo.objects.filter(user=request.session.get("_auth_user_id"))
            if len(user_additional) == 0:
                UserAdditionalInfo.objects.create(
                    user=User.objects.get(pk=self.user_id),
                    balance=0,
                    finished_tests_count=0
                )

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_id"] = self.user_id
        tests = Tests.objects.all()
        context["tests"] = tests
        return context


class Test(BaseView, TemplateView):
    template_name = "core/test.html"

    def get(self, request, test_id, *args, **kwargs):
        if not request.session.keys():
            return HttpResponseRedirect(reverse("auth_page"))

        if len(Tests.objects.filter(pk=test_id)) == 0:
            return HttpResponseNotFound("Такой тест не найден")
        else:
            kwargs["test_id"] = test_id
        return super().get(request, *args, **kwargs)

    def post(self, request, test_id, *args, **kwargs):
        answers = dict()
        for param_key in request.POST:
            if param_key != "csrfmiddlewaretoken":
                answers[param_key] = request.POST[param_key]

        current_user = User.objects.get(pk=request.session.get("_auth_user_id"))
        Answers.objects.create(
            answers=json.dumps(answers),
            user=current_user,
            test=Tests.objects.get(pk=test_id)
        )
        right_questions_count = int()
        questions = Questions.objects.filter(test=test_id)
        for answer in answers:
            for question in questions:
                if question.pk == int(answer):
                    if question.answer == answers[answer]:
                        right_questions_count += 1

        user_data = UserAdditionalInfo.objects.filter(user=current_user)
        current_balance = user_data[0].balance
        current_finished_tests_count = user_data[0].finished_tests_count
        new_balance = current_balance + 10
        new_finished_tests_count = current_finished_tests_count + 1
        user_data.update(balance=new_balance, finished_tests_count=new_finished_tests_count)

        return render(request, "core/test_finished.html",\
                      context={"right_questions_count": right_questions_count, "questions_count": len(questions)}
                      )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["questions"] = Questions.objects.filter(test=kwargs["test_id"])
        return context


class Stats(BaseView, TemplateView):
    template_name = "core/stats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all()
        context["users"] = dict()
        for user in users:
            additional_info = UserAdditionalInfo.objects.filter(user=user.pk)
            if len(additional_info) != 0:
                additional_info = additional_info[0]
            else:
                continue
            context["users"][user.username] = {"balance": additional_info.balance,\
                                         "finished_tests_count": additional_info.finished_tests_count}
        return context
