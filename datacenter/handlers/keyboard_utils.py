from telegram import ReplyKeyboardMarkup, KeyboardButton
from .static_text import main_menu_button_text
#from datacenter.models import Cake, Topping, Shape, Layer, Berries, Decor


def build_menu(buttons, n_cols):
    return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    print('make_start_keyboard')

    start_button_text = ['Следующий рецепт', 'Подписка']
    buttons = [KeyboardButton(button) for button in start_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_keyboard() -> ReplyKeyboardMarkup:
    print('make_keyboard_menu')
    button_text = ['Рецепт дня', 'Подписка']
    buttons = [KeyboardButton(choose) for choose in button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup
