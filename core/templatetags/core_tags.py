from django import template
from django.contrib.auth.models import User


register = template.Library()


def get_username_by_id(user_id: int or None):
    return User.objects.get(pk=user_id).username


register.filter("get_username_by_id", get_username_by_id)
