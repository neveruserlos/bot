
from telebot import types

item_settings = types.InlineKeyboardButton(text='Настроить ботика', callback_data='settings')
item_ins = types.InlineKeyboardButton(text='Инструкция', callback_data='ins')
item_yes = types.InlineKeyboardButton(text='Хочу!!!', callback_data='yes')