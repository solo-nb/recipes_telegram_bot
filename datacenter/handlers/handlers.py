from datetime import datetime, timedelta
from telegram import Update
from telegram.ext import ConversationHandler, CallbackContext
from django.utils import timezone
import random
from . import static_text
from datacenter.models import Users, Recipes, Types_of_recipes, Recipes_ingredients
from .keyboard_utils import make_keyboard_for_start_command, make_main_menu_keyboard, make_pay_menu_keyboard, make_pay_menu_keyboard2, make_category_menu_keyboard
from yoomoney import Quickpay
import webbrowser


INFO, MAIN_MENU, PAY, CATEGORY_MENU = range(4)


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
    customer_choise = update.message.text

    if customer_choise == static_text.pay_buttons[0]:
        update.message.reply_text(text='Оплата подписки', reply_markup=make_pay_menu_keyboard2())
        return PAY

    return MAIN_MENU


def get_main_menu(update: Update, context):
    print('get_customer_menu')
    customer_choise = update.message.text
    user_info = update.message.from_user.to_dict()
    user = Users.objects.get(telegram_id=user_info['id'])

    if customer_choise == static_text.main_menu_button_text[0]:

        print('Recipes')
        if user.subscription_to:
            time_user = user.subscription_to.strftime('%Y-%m-%d %H:%M:%S')
        else:
            time_user = datetime(2023, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
        time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if time_user > time_now:

            recipes = Recipes.objects.filter(is_subscribed=True)
            recipe = random.choice(recipes)
            with open (recipe.image, 'rb') as file:
                update.message.reply_photo(photo=file)
            update.message.reply_text(text='С подпиской')
            update.message.reply_text(text=recipe.name)
            update.message.reply_text(text=recipe.discription)

        else:
            recipes = Recipes.objects.filter(is_subscribed=False)
            recipe = random.choice(recipes)
            with open (recipe.image, 'rb') as file:
                update.message.reply_photo(photo=file)
            update.message.reply_text(text='Без подписки')
            update.message.reply_text(text=recipe.name)
            update.message.reply_text(text=recipe.discription)

        context.bot_data['recipe'] = recipe
        update.message.reply_text(text='Рецепт дня', reply_markup=make_main_menu_keyboard())
        return MAIN_MENU

    elif customer_choise == static_text.main_menu_button_text[1]:

        if not context.bot_data['recipe']:
            update.message.reply_text(text='Не выбран рецепт дня',reply_markup=make_main_menu_keyboard())
            return MAIN_MENU

        dish = context.bot_data['recipe']
        message_text = f'<b>Ингридиенты для {dish.name}:</b>'
        for _item in dish.ingredients.all():
            ingridient = Recipes_ingredients.objects.get(recipes=dish, ingredients=_item)
            message_text = message_text + f'\n  -{_item.name} (<i>{ingridient.quantity} {_item.unit}</i>)'    
        with open(dish.image, 'rb') as photo:
            update.message.reply_photo(photo=photo, caption=message_text, reply_markup=make_main_menu_keyboard(), parse_mode="HTML")
        
        return MAIN_MENU


    elif customer_choise == static_text.main_menu_button_text[2]:
        update.message.reply_text(text='Категория')
        update.message.reply_text(text='И тут', reply_markup=make_category_menu_keyboard())
        return CATEGORY_MENU


    elif customer_choise == static_text.main_menu_button_text[3]:
        if user.subscription_to:
            time = user.subscription_to.strftime('%Y-%m-%d %H:%M:%S')
            text = f'Подписка закончится:\n{time}'
        else:
            text = 'У вас нет подписки'
        update.message.reply_text(text=text, reply_markup=make_pay_menu_keyboard())
        return INFO
    
    elif customer_choise == static_text.main_menu_button_text[4]: # like
        update.message.reply_text(text='Спасибо за вашу оценку. Мы стремимся стать лучше', reply_markup=make_main_menu_keyboard())

    elif customer_choise == static_text.main_menu_button_text[5]: #dislike
        update.message.reply_text(text='Спасибо за вашу оценку. Мы стремимся стать лучше', reply_markup=make_main_menu_keyboard())

    else:
        update.message.reply_text(text=static_text.not_text_enter, reply_markup=make_main_menu_keyboard())
        return MAIN_MENU # Вернет меню на случай ручного ввода


def get_pay_menu(update: Update, cake_description):
    print('Оплата')

    customer_choise = update.message.text
    user_info = update.message.from_user.to_dict()
    user = Users.objects.get(telegram_id=user_info['id'])

    if customer_choise == static_text.main_pay_button_text[0]:
        user.subscription_to = datetime.now() + timedelta(hours=1)
        price = 1000

    if customer_choise == static_text.main_pay_button_text[1]:
        user.subscription_to = datetime.now() + timedelta(minutes=10)
        price = 600

    if customer_choise == static_text.main_pay_button_text[2]:
        user.subscription_to = datetime.now() + timedelta(minutes=5)
        price = 150

    quickpay = Quickpay(
        receiver="410013489645837",
        quickpay_form="shop",
        targets="Sponsor this project",
        paymentType="SB",
        sum=price,
        label=user
        )
    
    user.save()
    text = f'Подписка до:\n{user.subscription_to}'
    update.message.reply_text(text=text, reply_markup=make_main_menu_keyboard())

    print(quickpay.base_url)
    webbrowser.open(quickpay.base_url)

    return MAIN_MENU # Вернет меню на случай ручного ввода


def get_category_menu(update: Update, _):
    print('Категории')

    customer_choise = update.message.text
    print(customer_choise)
 
    text = f'Выборка по категории:\n{customer_choise}'
    update.message.reply_text(text=text, reply_markup=make_main_menu_keyboard())
    return MAIN_MENU # Вернет меню на случай ручного ввода


def command_cancel(update: Update, _):
    print('command_cancel')
    update.message.reply_text(text=static_text.cancel_text)
    return ConversationHandler.END
