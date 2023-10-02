from telegram import ReplyKeyboardMarkup, KeyboardButton
from .static_text import start_button_text, main_menu_button_text, pay_buttons, main_pay_button_text
from datacenter.models import Types_of_recipes


def build_menu(buttons, n_cols):
    return [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]


def make_keyboard_for_start_command() -> ReplyKeyboardMarkup:
    print('make_keyboard_for_start_command')
    buttons = [KeyboardButton(button) for button in start_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=1),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_main_menu_keyboard() -> ReplyKeyboardMarkup:
    print('make_main_menu_keyboard')
    buttons = [KeyboardButton(choose) for choose in main_menu_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_pay_menu_keyboard() -> ReplyKeyboardMarkup:
    print('make_pay_menu_keyboard')
    buttons = [KeyboardButton(choose) for choose in pay_buttons]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=1),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup

def make_pay_menu_keyboard2() -> ReplyKeyboardMarkup:
    print('make_pay_menu_keyboard2')
    buttons = [KeyboardButton(choose) for choose in main_pay_button_text]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=1),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup


def make_category_menu_keyboard() -> ReplyKeyboardMarkup:
    print('make_category_menu_keyboard')
    buttons = []
    category_buttons = Types_of_recipes.objects.all()
    for button in category_buttons:
        buttons.append(button.name)
    buttons = [KeyboardButton(choose) for choose in buttons]

    reply_markup = ReplyKeyboardMarkup(
        build_menu(buttons, n_cols=2),
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return reply_markup
