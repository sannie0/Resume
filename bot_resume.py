import telebot
from telebot import types
from collections import defaultdict
import time
import re
from datetime import datetime


TOKEN = "6965495172:AAGz4jNrcHZgu7hU6LPMedwUkr5-3bj63T8"
bot = telebot.TeleBot(TOKEN)

user_data = defaultdict(dict)

STEP = 0

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "Привет! Я помогу тебе составить резюме на твой вкус.\n\n"
        "Вот шаги, которые тебе нужно выполнить:\n"
        "1. Нажми /start для начала работы.\n"
        "2. Выбери шаблон.\n"
        "3. Следуй инструкциям для заполнения информации.\n"
        "4. Получи свое профессиональное резюме!"
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(commands=['start'])
def main(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)
    button_create_resume = types.InlineKeyboardButton(text='Составить резюме', callback_data='create_resume')
    markup_inline.add(button_create_resume)
    bot.send_message(message.chat.id, f'<b>Привет, {message.from_user.username}!</b>\n\n'
                                      'Я помогу тебе составить резюме на твой вкус📄\n\n'
                                      'Нажми на кнопку ниже, чтобы начать👇', parse_mode='html', reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call: call.data.startswith('template_'))
def choose_template(call):
    template_number = int(call.data.split('_')[1])

    # Сохраняем выбранный шаблон в данных пользователя
    user_id = call.from_user.id
    user_data[user_id]['template'] = template_number

    # Удаляем клавиатуру после выбора шаблона
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=None)

    bot.send_message(call.message.chat.id, f'«Шаблон {template_number}» выбран успешно! ✅\n'
                                           'Теперь мы можем перейти к следующему шагу.')

    personal_info(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'create_resume')
def create_resume(call):
    global STEP
    STEP += 1
    # Удаляем текущее сообщение
    bot.delete_message(call.message.chat.id, call.message.message_id)
    # Отправляем следующий блок с шагом 1 из 9
    bot.send_message(call.message.chat.id, '<b>Шаг 1 из 5.</b> Выбор шаблона.', parse_mode='html')

    # Создаем массив с медиа-группой (фотографии)
    media_group = []
    markup_inline = types.InlineKeyboardMarkup()

    for i in range(1, 6):
        photo_path = f'/Users/annasemenova/Desktop/рабочий стол/проектная деятельность/image/{i}.jpg'
        media_group.append(types.InputMediaPhoto(media=open(photo_path, 'rb')))

    button1 = types.InlineKeyboardButton(text='Шаблон 1', callback_data='template_1')
    markup_inline.add(button1)

    # Добавляем кнопки выбора шаблона
    for i in range(2, 6, 2):
        button_left = types.InlineKeyboardButton(text=f'Шаблон {i}', callback_data=f'template_{i}')
        button_right = types.InlineKeyboardButton(text=f'Шаблон {i + 1}', callback_data=f'template_{i + 1}')
        markup_inline.add(button_left, button_right)

    bot.send_media_group(call.message.chat.id, media=media_group)
    bot.send_message(call.message.chat.id, 'Для того, чтобы создать резюме, выбери шаблон, который тебе нравится📋',
                     reply_markup=markup_inline)

def show_progress(chat_id):
    user_id = chat_id
    progress_message = f'<b>Промежуточный результат:</b>\n\n'

    if 'template' in user_data[user_id]:
        progress_message += f'Шаблон: {user_data[user_id]["template"]}\n'
    if 'name' in user_data[user_id]:
        progress_message += f'Имя: {user_data[user_id]["name"]}\n'
    if 'lastname' in user_data[user_id]:
        progress_message += f'Фамилия: {user_data[user_id]["lastname"]}\n'
    if 'patr' in user_data[user_id]:
        progress_message += f'Отчество: {user_data[user_id]["patr"]}\n'
    if 'email' in user_data[user_id]:
        progress_message += f'Электронная почта: {user_data[user_id]["email"]}\n'
    if 'phone' in user_data[user_id]:
        progress_message += f'Номер телефона: {user_data[user_id]["phone"]}\n'
    if 'citizenship' in user_data[user_id]:
        progress_message += f'Гражданство: {user_data[user_id]["citizenship"]}\n'
    if 'birthdate' in user_data[user_id]:
        progress_message += f'Дата рождения: {user_data[user_id]["birthdate"]}\n'
    if 'gender' in user_data[user_id]:
        progress_message += f'Пол: {user_data[user_id]["gender"]}\n'
    if 'status' in user_data[user_id]:
        progress_message += f'Семейное положение: {user_data[user_id]["status"]}\n'
    if 'city' in user_data[user_id]:
        progress_message += f'Город проживания: {user_data[user_id]["city"]}\n'
    if 'univ' in user_data[user_id]:
        progress_message += f'Учебное заведение: {user_data[user_id]["univ"]}\n'
    if 'facultate' in user_data[user_id]:
        progress_message += f'Факультет: {user_data[user_id]["facultate"]}\n'
    if 'formed' in user_data[user_id]:
        progress_message += f'Форма обучения: {user_data[user_id]["formed"]}\n'
    if 'year' in user_data[user_id]:
        progress_message += f'Год окончания: {user_data[user_id]["year"]}\n'
    if 'prof' in user_data[user_id]:
        progress_message += f'Специальность: {user_data[user_id]["prof"]}\n'
    if 'post' in user_data[user_id]:
        progress_message += f'Должность: {user_data[user_id]["post"]}\n'
    if 'exp' in user_data[user_id]:
        progress_message += f'Опыт работы: {user_data[user_id]["exp"]}\n'
    if 'dopinf' in user_data[user_id]:
        progress_message += f'Дополнительная инфорамация: {user_data[user_id]["dopinf"]}\n'
    if 'link' in user_data[user_id]:
        progress_message += f'Ссылки: {user_data[user_id]["link"]}\n'

    bot.send_message(chat_id, progress_message, parse_mode='html')

    markup_inline = types.InlineKeyboardMarkup()
    button_yes = types.InlineKeyboardButton(text='Да', callback_data='confirm_resume_generation')
    button_no = types.InlineKeyboardButton(text='Нет', callback_data='cancel_resume_generation')
    markup_inline.add(button_yes, button_no)

    # Отправляем текст с кнопками
    bot.send_message(chat_id, 'Сгенерировать резюме?', reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call: True)
def handle_confirmation_callback(call):
    user_id = call.from_user.id

    if call.data == 'confirm_resume_generation':
        #Обработка подтверждения генерации резюме
        # ...
        bot.send_message(call.message.chat.id, 'В разработке😊')


    elif call.data == 'cancel_resume_generation':
        # Очистка словаря при отказе от генерации резюме
        user_data.pop(user_id, None)
        bot.send_message(call.message.chat.id, 'Ты отменил создание резюме. Данные были удалены😔')

def personal_info(chat_id):
    bot.send_message(chat_id, f'<b>Шаг 2 из 5</b>. Личная информация.\n', parse_mode='html')
    bot.send_message(chat_id, 'Напиши свое полное имя.')

def ask_for_email(chat_id):
    bot.send_message(chat_id, 'Укажи свою электронную почту.')

def ask_for_phone(chat_id):
    bot.send_message(chat_id, 'Укажи свой номер телефона.')

def is_valid_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email)

def is_valid_phone(phone):
    phone_regex = r'^\+(\d{1,15})$'
    return re.match(phone_regex, phone)

def ask_for_citizenship(chat_id):
    bot.send_message(chat_id, 'Укажи свое гражданство.')

def ask_for_birthdate(chat_id):
    bot.send_message(chat_id, 'Укажи свою дату рождения в формате __.__.____ .')

def is_valid_birthdate(birthdate):
    try:
        date_object = datetime.strptime(birthdate, '%d.%m.%Y')
        if 1960 <= date_object.year <= 2023:
            return True
        else:
            return False
    except ValueError:
        return False

def ask_for_gender(chat_id):
    bot.send_message(chat_id, 'Укажи свой пол.')

def ask_for_status(chat_id):
    bot.send_message(chat_id, 'Укажи свое семейное положение.')

def ask_for_city(chat_id):
    bot.send_message(chat_id, 'Укажи город проживания.')

def ask_for_univ(chat_id):
    bot.send_message(chat_id, 'Укажи свое учебное заведение.')

def ask_for_facultate(chat_id):
    bot.send_message(chat_id, 'Укажи свой факультет.')

def ask_for_formed(chat_id):
    bot.send_message(chat_id, 'Укажи свою форму обучения.')

def ask_for_year(chat_id):
    bot.send_message(chat_id, 'Укажи год окончания университета.')

def ask_for_prof(chat_id):
    bot.send_message(chat_id, 'Укажи свою специальность.')

def ask_for_post(chat_id):
    bot.send_message(chat_id, 'Укажи прошлую должность.')

def ask_for_exp(chat_id):
    bot.send_message(chat_id, 'Укажи опыт работы.')

def ask_for_dopinf(chat_id):
    bot.send_message(chat_id, 'Укажи свои профессиональные знания и навыки.')

def ask_for_link(chat_id):
    bot.send_message(chat_id, 'Укажи ссылки на портфолио или профессиональный аккаунт.')

def edit_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    item1 = types.KeyboardButton('Шаг 1')
    item2 = types.KeyboardButton('Шаг 2')
    item3 = types.KeyboardButton('Шаг 3')
    item4 = types.KeyboardButton('Шаг 4')
    item5 = types.KeyboardButton('Шаг 5')
    item6 = types.KeyboardButton('Назад')

    markup.add(item1, item2, item3, item4, item5, item6)

    bot.send_message(chat_id, 'Меню редактирования:', reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def get_personal_info(message):
    global STEP
    user_id = message.from_user.id

    if 'name' not in user_data[user_id]:
        # Пользователь вводит имя
        name_parts = message.text.split()
        if len(name_parts) == 3:
            if name_parts[0].isalpha() and name_parts[1].isalpha() and name_parts[2].isalpha():
                user_data[user_id]['name'] = name_parts[0].capitalize()
                user_data[user_id]['lastname'] = name_parts[1].capitalize()
                user_data[user_id]['patr'] = name_parts[2].capitalize()
                STEP += 1
                ask_for_email(message.chat.id)  # 2 вопрос
            else:
                bot.send_message(message.chat.id,'Допускаются только буквы.')
        else:
            bot.send_message(message.chat.id,'Пожалуйста, введи свое полное имя, состоящее из трех слов (имя, фамилия, отчество).')
    elif 'email' not in user_data[user_id]:
        email = message.text.strip()

        if is_valid_email(email):
            user_data[user_id]['email'] = email
            STEP += 1
            ask_for_phone(message.chat.id)#3 вопрос
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введи свою электронную почту в правильном формате.')
    elif 'phone' not in user_data[user_id]:
        # Пользователь вводит номер телефона
        phone = message.text.strip()

        if is_valid_phone(phone):
            if len(phone) == 12:
                user_data[user_id]['phone'] = phone
                STEP += 1
                ask_for_citizenship(message.chat.id)#4 вопрос
            else:
                bot.send_message(message.chat.id, 'Номер слишком короткий')
        else:
            # Если номер телефона введен в неправильном формате, просим пользователя ввести правильный формат
            bot.send_message(message.chat.id, 'Пожалуйста, введи свой номер телефона в правильном формате: +7')
    elif 'citizenship' not in user_data[user_id]:
        citizenship = message.text.strip()
        user_data[user_id]['citizenship'] = citizenship
        STEP += 1
        #ask_for_birthdate(message.chat.id)
    elif 'birthdate' not in user_data[user_id]:
        birthdate = message.text.strip()
        print(birthdate)
        if is_valid_birthdate(birthdate):
            user_data[user_id]['birthdate'] = birthdate

            ask_for_gender(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введи свою дату рождения в правильном формате.')
    elif 'gender' not in user_data[user_id]:
        gender = message.text.strip()
        if gender.lower() == 'женский' or gender.lower() == 'мужской':

            user_data[user_id]['gender'] = gender.capitalize()

            ask_for_status(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введи либо женский, либо мужской.')

    elif 'status' not in user_data[user_id]:
        status = message.text.strip()

        if all(word.isalpha() or word.isspace() for word in status.split()):
            user_data[user_id]['status'] = status.capitalize()
            ask_for_city(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'city' not in user_data[user_id]:
        city = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in city.split()):
            user_data[user_id]['city'] = city.capitalize()
            bot.send_message(message.chat.id, '<b>Шаг 3 из 5.</b> Образование.', parse_mode='html')

            ask_for_univ(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'univ' not in user_data[user_id]:
        univ = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in univ.split()):
            user_data[user_id]['univ'] = univ
            ask_for_facultate(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'facultate' not in user_data[user_id]:
        facultate = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in facultate.split()):
            user_data[user_id]['facultate'] = facultate.capitalize()
            ask_for_formed(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'formed' not in user_data[user_id]:
        formed = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in formed.split()):
            user_data[user_id]['formed'] = formed.capitalize()
            ask_for_year(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')

    elif 'year' not in user_data[user_id]:
        year = message.text.strip()
        if year.isdigit() and int(year) > 1980:
            user_data[user_id]['year'] = year
            ask_for_prof(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Пожалуйста, введи правильный год.')


    elif 'prof' not in user_data[user_id]:
        prof = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in prof.split()):
            user_data[user_id]['prof'] = prof.capitalize()

            bot.send_message(message.chat.id, '<b>Шаг 4 из 5.</b> Опыт работы.', parse_mode='html')
            ask_for_post(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'post' not in user_data[user_id]:
        post = message.text.strip()
        if all(word.isalpha() or word.isspace() for word in post.split()):
            user_data[user_id]['post'] = post.capitalize()
            ask_for_exp(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Допускаются только буквы.')


    elif 'exp' not in user_data[user_id]:
        exp = message.text.strip()
        user_data[user_id]['exp'] = exp.capitalize()
        ask_for_dopinf(message.chat.id)

    elif 'dopinf' not in user_data[user_id]:
        dopinf = message.text.strip()
        if len(dopinf) > 120:
            user_data[user_id]['dopinf'] = dopinf
            ask_for_link(message.chat.id)
        else:
            bot.send_message(message.chat.id, 'Сообщение должно содержать более 120 символов', parse_mode='html')


    elif 'link' not in user_data[user_id]:
        link = message.text.strip()
        user_data[user_id]['link'] = link

        bot.send_message(message.chat.id, '<b>Шаг 5 из 5.</b> Почти готово!', parse_mode='html')

        show_progress(message.chat.id)
        """


    if STEP == 5:
        edit_menu({'message': {'chat': {'id': user_id}}})"""



bot.polling(none_stop=True)
