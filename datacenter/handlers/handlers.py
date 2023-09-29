from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext

#from . import static_text
from datacenter.models import Users
from .keyboard_utils import make_keyboard_for_start_command, make_keyboard

INFO, SUBSCRIPTION = range(2)


def command_start(update: Update, context):
    print('command_start')

   # user, created = Users.objects.get_or_create(telegram_id=user_info['id'], username=user_info['username'])

    text = 'Привет, !Добро пожаловать в бот с вкуными рецептами'

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
        reply_markup=make_keyboard(),
    )
    return INFO

def get_info(update: Update, context):
    command_menu = update.message.text
    print(update.message.text)
    if command_menu == 'Рецепт дня':
        print('Рецепт дня')
        update.message.reply_text(text='Rexf htwtgnjd', reply_markup=make_keyboard())
        return INFO
    if command_menu == 'Подписка':
        print('Подписка')
        update.message.reply_text(text='', reply_markup=make_keyboard())
        return SUBSCRIPTION


def get_subscription(update: Update, context):
    pass


def command_cancel(update: Update, _):
    print('command_cancel')
    update.message.reply_text(text=static_text.cancel_text)
    return ConversationHandler.END
