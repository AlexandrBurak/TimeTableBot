import datetime as dt
import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Updater, Filters
from telegram.error import BadRequest


class EnvironVarException(Exception):
    pass


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if TELEGRAM_TOKEN is None:
    logging.critical('TELEGRAM_TOKEN отсутствует!')
    raise EnvironVarException

DATABASE = {
    'Monday': 'Понедельник\nОперационные системы 8.15-9.35 м507 508(Зенько)\nФизра 9.45-11.05\nТвимсы(лекция) 11.15-12.35 607\nМЧА(лекция) 13.00-14.20 605\nТвимсы 14.30-15.50 518 600г(Хаткевич)',
    'Tuesday': 'Вторник\nПолитология(лекция) 16.00-17.20 607\nПолитология(лекция) 17.30-18.50 607',
    'Wednesday': 'Среда\nДиффуры 8.15-9.35 517\nМатан(лекция) 9.45-11.05 605\nДиффуры(лекция) 11.15-12.35 607',
    'Thursday': 'Четверг\nФАиИу 9.45-11.05 513\nАлгосы(лекция) 11.15-12.35 607\nПолитология 13.00-14.20 600-г\nМЧА 14.30-15.50 519 600в(Будник)',
    'Friday': 'Пятничка\nАлгосы 8.15-9.35 м604\nФизра 9.45-11.05\nТвимсы(лекция) 11.15-12.35 605',
    'Saturday': 'Суббота\nОперационные системы(лекция) 8.15-9.35 607\nМатан 9.45-11.05 522\nФАиИУ(лекция) 11.15-12.35 607',
    'Sunday': 'Воскресенье\nПар нет!'}


def wake_up(update, context):
    """/start."""
    chat = update.effective_chat
    text = 'Приветствую!'
    button = ReplyKeyboardMarkup([['/nextpairs']])
    context.bot.send_message(chat_id=chat.id,
                             text=text,
                             reply_markup=button)
    logging.info(f'Сообщение отправлено:\n{text}')


def text_msg(update, context):
    """Another text"""
    chat = update.effective_chat
    text = 'Не дури головы!'
    button = ReplyKeyboardMarkup([['/nextpairs']])
    context.bot.send_message(chat_id=chat.id,
                             text=text,
                             reply_markup=button)
    logging.info(f'Сообщение отправлено:\n{text}')


def get_info():
    moment = dt.datetime.now()
    message = ''
    if int(moment.strftime("%H")) < 14:
        day = moment.strftime("%A")
        message = DATABASE.get(day)
    else:
        day = (moment + dt.timedelta(days=1)).strftime("%A")
        message = DATABASE.get(day)
    return message


def next_couple(update, context):
    message = get_info()
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([['/nextpairs']])
    try:
        context.bot.send_message(chat_id=chat.id,
                                 text=message,
                                 reply_markup=button)

        if chat.id != 906308821:
            try:
                context.bot.send_message(chat_id=906308821,
                                         text=f'Кто-то сделал запрос\n{chat.username}\n{chat.first_name}\n{chat.last_name}',
                                         reply_markup=button)
            except Exception:
                pass
            logging.info('Кто-то сделал запрос')
        logging.info(f'Сообщение отправлено:\n{message}')
    except BadRequest as ex:
        logging.error(f'Сообщение не отправлено: {ex}')
        context.bot.send_message(chat_id=chat.id,
                                 text=f'Сообщение не отправлено: {ex}',
                                 reply_markup=button)


def main():
    updater = Updater(token=TELEGRAM_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('nextpairs', next_couple))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_msg))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
