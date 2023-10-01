from django.contrib import admin
from datacenter.models import *


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['id', 'telegram_id', 'username', 'name', 'is_admin']
    search_fields = ['telegram_id', 'username']

@admin.register(Recipes)
class RecipesAdmin(admin.ModelAdmin):
    list_display = ['name', 'image', 'is_subscribed']
    raw_id_fields = ['types_of_recipes', 'ingredients']


@admin.register(Units)
class UnitsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Types_of_recipes)
class Types_of_recipesAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    list_display = ['name', 'unit', 'price']
    raw_id_fields = ['unit']


@admin.register(Recipes_ingredients)
class Recipes_ingredientsAdmin(admin.ModelAdmin):
    list_display = ['recipes', 'ingredients', 'quantity']
    raw_id_fields = ['recipes', 'ingredients']


admin.register(Grades)
class GradesAdmin(admin.ModelAdmin):
    list_display = ['user', 'recipes', 'grade']
    raw_id_fields = ['user', 'recipes']



# Register your models here.
