#!/usr/bin/env python
"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'assistant.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
try:
    from django.core.management import execute_from_command_line
except ImportError as exc:
    raise ImportError(
        "Couldn't import Django. Are you sure it's installed and "
        "available on your PYTHONPATH environment variable? Did you "
        "forget to activate a virtual environment?"
    ) from exc

from shoppinglist.models import Product
from django.utils import timezone
import pathlib
import logging
from telegram_secrets import TOKEN, CHAT_ID
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import functools

CURRENT_DIR = pathlib.Path().absolute()
SHOPPING_LIST = "/home/javier/src/python/assistant/shopping_list.txt"
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
@is_home_chat
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("I'm alive!")


def test_inline(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data='1'),
            InlineKeyboardButton("Option 2", callback_data='2'),
        ],
        [InlineKeyboardButton("Option 3", callback_data='3')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    query.edit_message_text(text="Selected option: {}".format(query.data))

@is_home_chat
def help_command(update, context):
    """Send a message when the command /help is issued."""
    help_message = """ Hola! Soy 1503 bot y estoy aqui para ayudarte a hacer la compra.
    -  Enviame tus articulos escribiendo /add <articulo>.
    -  Puedes recuperar la lista de la compra con el comando /list
    -  Tambien puedes borrar articulos con /rm o la lista completa con /clear.
    Pruebame y dame feedback, estoy aprendiendo!"""
    update.message.reply_text(help_message)


@is_home_chat
def delete_item(update, context):
    """Delete item from the shopping list"""
    if update.effective_chat.id != CHAT_ID:
        logger.info("Message from another chat:")
        return

    item_to_remove = update.message.text.replace("/rm", "").strip()

    with open(SHOPPING_LIST, "r") as f:
        lista = [item.strip() for item in f.read().splitlines()]
        lista.remove(item_to_remove)

    with open(SHOPPING_LIST, "w") as f:
        for item in lista:
            print(item, file=f, flush=True)

    # update.message.reply_text("item deleted", quote=False)


def is_home_chat(func):
    """Checks the message comes from our home's chat"""
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if args[0].effective_chat.id != CHAT_ID:
            logger.info("Message from another chat: ")
            return None
        else:
            return func(*args, **kwargs)
    return wrapper_decorator


@is_home_chat
def add_item(update, context):
    """Add item to the shopping list"""
    item_aded = update.message.text.replace("/add", "")
    with open(SHOPPING_LIST, "a") as f:
        print(item_aded, file=f, flush=True)
        logger.info("item added")

@is_home_chat
def get_list(update, context):
    """Get shopping list"""
    with open(SHOPPING_LIST, "r") as f:
        for item in f.read().splitlines():
            if item != '':
                update.message.reply_text(item, quote=False)

@is_home_chat
def clear_list(update, context):
    """Clear shopping list"""
    print(SHOPPING_LIST)
    os.remove(SHOPPING_LIST)
    with open(SHOPPING_LIST, "a") as _:
        logger.info("List created")


# def echo(update, context):
#     """Echo the user message."""
#     update.message.reply_text(update.message.text)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("add", add_item))
    dp.add_handler(CommandHandler("lista", get_list))
    dp.add_handler(CommandHandler("clear", clear_list))
    dp.add_handler(CommandHandler("rm", delete_item))
    dp.add_handler(CommandHandler("test", test_inline))
    dp.add_handler(CallbackQueryHandler(button))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
