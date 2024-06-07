import telebot
from telebot import types
import os
import json
from items import *

# Подставьте свой токен вместо TOKEN
from cfg import *

bot = telebot.TeleBot(TOKEN)

# Словарь с профессиональными эмодзи для каждого пользователя


# Функция для добавления пользователя в базу данных
def add_user_to_db(message):
    username = message.from_user.username
    filename = 'everyone.json'

    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            json.dump([], file)  # Создаем пустой список

    with open(filename, 'r') as file:
        data = json.load(file)

    if f'{username}' not in data:  # Проверяем, что пользователь не добавлен ранее
        data.append(f'{username}')  # Добавляем пользователя в список

    with open(filename, 'w') as file:
        json.dump(data, file)
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    add_user_to_db(message)
    markup_inline = types.InlineKeyboardMarkup()
    username = message.from_user.username
    user_id = message.from_user.id
    if user_id == 6466367023 or 5788301791 or 6034473264:
        emoji = '👤'  # Эмодзи по умолчанию, если нет соответствующего

        markup_inline.add(types.InlineKeyboardButton(text='Настройки', callback_data='settings'))
        markup_inline.add(types.InlineKeyboardButton(text='Да', callback_data='yes'))
        bot.send_message(message.chat.id, f'{emoji} Приветик {username}!\n\nХочешь немного печенек?🍪🍪🍪',
                         reply_markup=markup_inline)
    else:
        pass

# Обработчик текстовых сообщений

# Обработчик для команды /go
@bot.message_handler(commands=['go'])
def send_everyone(message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Проверяем, что команда пришла из разрешённых чатов
    if user_id in [6466367023, 5788301791, 6034473264]:
        filename = 'everyone.json'

        if os.path.exists(filename):
            with open(filename, 'r') as file:
                data = json.load(file)

            if data:
                text = message.text.split('/go', 1)[1].strip()  # Получаем текст после /go

                user_links = []
                for i, username in enumerate(data, start=1):
                    user_links.append(f'{text}\n\n' if i % 4 == 1 else '')  # Добавляем текст перед каждой четвёркой
                    user_links.append(f'[👤](https://t.me/{username})ㅤ')
                    # Каждые 4 ссылки отправляем в отдельном сообщении
                    if i % 4 == 0:
                        bot.send_message(chat_id, ''.join(user_links).strip(), parse_mode='MarkdownV2',
                                         disable_web_page_preview=True)
                        user_links = []  # Очищаем список для следующей четверки

                # Отправляем оставшиеся упоминания, если есть
                if user_links:
                    bot.send_message(chat_id, ''.join(user_links).strip(), parse_mode='MarkdownV2',
                                     disable_web_page_preview=True)
            else:
                bot.send_message(chat_id, "Список пользователей пуст")
        else:
            bot.send_message(chat_id, "Файл с пользователями не найден")
    else:
        print(f'{chat_id}')


@bot.message_handler(content_types=['text'])
def add(message):
    add_user_to_db(message)

# Обработчик для inline-кнопок
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    user_id = call.message.from_user.id
    username = call.from_user.username
    chat_id = call.message.chat.id
    markup_inline = types.InlineKeyboardMarkup()
    if user_id == 6466367023 or 5788301791 or 6034473264:
        if call.data == 'settings':
            markup_inline.add(item_ins)
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)
            bot.send_message(chat_id,
                             f'Вот настройки ботика @{username}:\n\nНастройки в зазывале?\nИх нет!\n\nЛучше посмотри инструкцию ниже:',
                             reply_markup=markup_inline)
        elif call.data == 'yes':
            bot.delete_message(chat_id=chat_id, message_id=call.message.message_id)

            photo_cookie = 'cookie.jpg'
            with open(photo_cookie, 'rb') as photo:
                markup_inline.add(item_settings)
                bot.send_photo(chat_id, photo, caption='Держи печеньку🍪', reply_markup=markup_inline)
        elif call.data == 'ins':
            markup_inline.add(item_settings)
            usernamee = call.from_user.first_name
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id,
                                  text=f'⸻⸻⸻⸻⸻⸻Инструкция⸻⸻⸻⸻⸻⸻ {usernamee}:\n\n/go\n\n\nБот:\n\nНачинаю призыв {usernamee}!',
                                  reply_markup=markup_inline)
    else:
        pass

# Запуск бота
bot.polling(none_stop=True)
