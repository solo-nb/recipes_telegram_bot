from telegram import Bot
from telegram.ext import (CommandHandler, ConversationHandler, Filters, MessageHandler, Updater, )
from recipes_telegram_bot.settings import TELEGRAM_TOKEN
from datacenter.handlers import handlers


bot_handlers = ConversationHandler(
    entry_points=[
        MessageHandler(Filters.regex('^(Старт)$'), handlers.get_info),
    ],
    states={
        handlers.INFO: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_info)
        ],
        handlers.SUBSCRIPTION: [
            MessageHandler(Filters.text & ~Filters.command, handlers.get_subscription)
        ],
    },
    fallbacks=[
        CommandHandler("cancel", handlers.command_cancel)
    ]
)


def setup_dispatcher(dp):
    dp.add_handler(bot_handlers)
    dp.add_handler(CommandHandler("start", handlers.command_start))
    return dp


def run_pooling():
    """ Run bot in pooling mode """
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp = setup_dispatcher(dp)

    bot_info = Bot(TELEGRAM_TOKEN).get_me()
    bot_link = f'https://t.me/{bot_info["username"]}'

    print(f"Pooling of '{bot_link}' started")

    updater.start_polling()
    updater.idle()
