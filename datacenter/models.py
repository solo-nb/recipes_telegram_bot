import uuid
from django.db import models
from django.utils import timezone


class TimeStampedMixin(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Users(UUIDMixin, TimeStampedMixin):
    telegram_id = models.IntegerField(unique=True, default=False)
    username = models.CharField(max_length=64, null=True, verbose_name='UserName')
    name = models.CharField(max_length=256, null=True, verbose_name='Имя')
    is_admin = models.BooleanField(null=True, blank=True, default=False, verbose_name='Администратор')
    registration = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'