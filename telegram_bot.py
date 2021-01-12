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
import logging
import functools
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "assistant.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from telegram_secrets import TOKEN, CHAT_ID
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext
)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from shoppinglist.models import ShoppingList, Product

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def is_home_chat(func):
    """Checks the message comes from our home's chat"""

    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        if args[0].effective_chat.id != CHAT_ID:
            logger.info("Message from another chat: ")
            return None
        return func(*args, **kwargs)

    return wrapper_decorator


@is_home_chat
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text("I'm alive!")


def test_inline(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose:", reply_markup=reply_markup)


def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification
    # to the user is needed
    # Some clients may have trouble otherwise. See
    # https://core.telegram.org/bots/api#callbackquery
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
def add_item(update, context):
    """Add item to the shopping list"""
    product_to_add = update.message.text.replace("/add ", "").strip()
    current_shopping_list = ShoppingList.get_current_list()
    try:
        product = Product.objects.get(name=product_to_add)
    except Product.DoesNotExist:
        product = Product(name=product_to_add)
        product.save()
        product.shopping_list.add(current_shopping_list)
    product.shopping_list.add(current_shopping_list)

    logger.info("%s added", product_to_add)


@is_home_chat
def delete_item(update, context):
    """Delete item from the shopping list"""
    product_to_remove = update.message.text.replace("/rm", "").strip()
    current_shopping_list = ShoppingList.get_current_list()
    try:
        product = Product.objects.get(name=product_to_remove)
    except Product.DoesNotExist:
        product = Product(name=product_to_remove)
        product.save()

    product.shopping_list.only().delete()

    logger.info("%s deleted", product_to_remove)


@is_home_chat
def get_list(update, context):
    """Get shopping list"""
    items_list = ShoppingList.get_current_list().list_items()
    for item in items_list:
        update.message.reply_text(item, quote=False)

    logger.info("Current list requested")


@is_home_chat
def clear_list(update, context):
    """Clear shopping list"""
    ShoppingList.get_current_list().clear_list()

    logger.info("Current list emptied")


@is_home_chat
def mark_list_as_done(update, context):
    """Mark shopping list as purchased"""
    ShoppingList.get_current_list().mark_list_as_done()


def main():
    """Start the bot."""
    updater = Updater(TOKEN)

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

    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
