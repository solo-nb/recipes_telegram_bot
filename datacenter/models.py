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
    username = models.CharField(
        max_length=64, null=True, verbose_name='UserName')
    name = models.CharField(max_length=256, null=True, verbose_name='Имя')
    is_admin = models.BooleanField(
        null=True, blank=True, default=False, verbose_name='Администратор')
    registration = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.username:
            return f'@{self.username}'
        else:
            return f'{self.telegram_id}'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Types_of_recipes(models.Model):
    name = models.CharField(max_length=150)


class Recipes(models.Model):
    name = models.CharField(max_length=150)
    discription = models.CharField(max_length=1024)
    types_of_recipes = models.ForeignKey(
        Types_of_recipes, on_delete=models.SET_NULL, null=True)
    is_subscribed = models.BooleanField()
    ingredients = models.ManyToManyField('Ingredients',
                                         through='Recipes_ingredients')


class Units(models.Model):
    name = models.CharField(max_length=150)


class Ingredients(models.Model):
    name = models.CharField(max_length=150)
    unit = models.ForeignKey(Units, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()


class Recipes_ingredients(models.Model):
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredients = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.FloatField()


class Grades(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    recipes = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    grade = models.BooleanField()
