from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

from . import static_text
from datacenter.models import Users, Recipes
from .keyboard_utils import make_keyboard_for_start_command, make_main_menu_keyboard, make_pay_menu_keyboard, make_pay_menu_keyboard2


INFO, MAIN_MENU, PAY, ORDER_CAKE, LAYER, DECOR, TOPPING, BERRIES, CALCULATE, COMPLAINT, COMPLAINT_TEXT = range(11)


def command_start(update: Update, context):
    print('command_start')
    if update.message:
        user_info = update.message.from_user.to_dict()
    else:
        user_info = {'id': context.user_data['user_id'], 'username': context.user_data['username'],
                     'first_name': context.user_data['first_name']}

    user, created = Users.objects.get_or_create(telegram_id=user_info['id'], username=user_info['username'])

    if created:
        text = static_text.start_created.format(first_name=user_info['first_name'])
    else:
        text = static_text.start_not_created.format(first_name=user_info['first_name'])

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=make_keyboard_for_start_command(),
    )
    return MAIN_MENU


def get_info(update: Update, _: CallbackContext):
    print('info')
    update.message.reply_text(text='Подписка закончится')
    update.message.reply_text(text='Подписка', reply_markup=make_pay_menu_keyboard2())

    return MAIN_MENU
    

def get_main_menu(update: Update, _):
    print('get_customer_menu')
    customer_choise = update.message.text
    if customer_choise == static_text.main_menu_button_text[0]:
        print('get_order')
        update.message.reply_text(text='Рецепт дня',reply_markup=make_main_menu_keyboard())
        recipes = Recipes.objects.all()
        return MAIN_MENU
    elif customer_choise == static_text.main_menu_button_text[1]:
        update.message.reply_text(text='Тут будет подписка', reply_markup=make_pay_menu_keyboard())
        return INFO
    elif customer_choise == static_text.main_menu_button_text[2]:
        update.message.reply_text(text='Тут контакты')
        update.message.reply_text(text='И тут', reply_markup=make_main_menu_keyboard())
        return MAIN_MENU
    else:
        update.message.reply_text(text=static_text.not_text_enter, reply_markup=make_main_menu_keyboard())
        return MAIN_MENU # Вернет меню на случай ручного ввода


#def get_pay_menu(update: Update, cake_description):
#    pass 
#    return MAIN_MENU # Вернет меню на случай ручного ввода


def command_cancel(update: Update, _):
    print('command_cancel')
    update.message.reply_text(text=static_text.cancel_text)
    return ConversationHandler.END
