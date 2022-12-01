from django.contrib import admin
from .models import Tests, Questions, Answers, UserAdditionalInfo


class TestsAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("id", "title")


class QuestionsAdmin(admin.ModelAdmin):
    list_display = ("id", "question_text", "answer", "test")
    list_display_links = ("id", "question_text", "answer", "test")
    search_fields = ("test", "question_text", "id")


class AnswersAdmin(admin.ModelAdmin):
    list_display = ("id", "answers", "user", "test")
    list_display_links = ("id", "answers", "user", "test")
    search_fields = ("id", "answers", "user", "user")


class UserAdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "balance", "user", "finished_tests_count")
    list_display_links = ("id", "balance", "user", "finished_tests_count")
    search_fields = ("id", "balance", "user", "finished_tests_count")


admin.site.register(Tests, TestsAdmin)
admin.site.register(Questions, QuestionsAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(UserAdditionalInfo, UserAdditionalInfoAdmin)
