from telebot import types
import telebot
import time 
import random 
import math 


token = "7931021196:AAE8W9bmiAJU7aZIV5SbWrNG6W0EmaHnd4Y"

bot = telebot.TeleBot(token)

pets = {}


def create_pet(name, type):
    return {
        "name": name,
        "type": type,
        "happines": 50,
        "energy": 50,
        "hunger": 50,
        "coins": 0,
        "last_update": time.time(),
        "is_sleep": False
    }


def create_main():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Покормить", "Поиграть")
    markup.row("Спать", "Статус", "Монеты")
    return markup


def process_name(message):
    name = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Кошка", "Собака")
    markup.row("Капибара", "Змея")
    bot.send_message(message.chat.id, text=f'{message.from_user.first_name} дальше нужно будет выбрать тип питомца: ',
                     reply_markup=markup)
    bot.register_next_step_handler(message, process_register, name)


def process_register(message, name):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Твой питомец создан", reply_markup=create_main())
    type = message.text
    pets[chat_id] = create_pet(name, type)
    print(pets[chat_id])


def update_pet(pet):
    current_update = time.time()
    time_pass = current_update - pet["last_update"]

    pet['hunger'] = min(100, max(0, pet['hunger'] + 0.1 * time_pass))
    if not pet["is_sleep"]:
        pet["energy"] = min(100, max(0, pet["energy"] - 0.05 * time_pass))
        pet["happines"] = min(100, max(0, pet["happines"] - 0.05 * time_pass))
    else:
        pet["energy"] = min(100, max(0, pet["energy"] + 0.05 * time_pass))

    pet["last_update"] = current_update


def feed_pet(pet):
    pet['hunger'] = max(0, pet['hunger'] - 10)
    pet['coins'] += 5


def play_pet(pet):
    pet["happines"] = min(100, pet["happines"] + 10)
    pet["energy"] = max(0, pet["energy"] - 20)
    pet['coins'] += 10
    global a
    a=random.randint(0,10)
    if a>5:
        pet['coins'] +=20



def sleep_pet(pet):
    pet["is_sleep"] = not pet["is_sleep"]
    pet["energy"] = max(0, pet["energy"] + 50)


@bot.message_handler(commands=['start'])
def start(message):
    text = f"Привет, {message.from_user.first_name}, давай назовем твоего питомца: "
    msg = bot.send_message(message.chat.id, text=text)
    bot.register_next_step_handler(msg, process_name)


@bot.message_handler(func=lambda message: True)
def actions(message):
    chat_id = message.chat.id
    pet = pets.get(chat_id)

    if not pet:
        bot.send_message(chat_id, "Сначала нужно создать питомца через команду /start")
        return

    update_pet(pet)

    if message.text == "Покормить":
        feed_pet(pet)
        bot.send_message(chat_id, f"Питомец {pet['name']} поел! Он заработал 5 монет")
    elif message.text == "Поиграть":
        play_pet(pet)
        bot.send_message(chat_id, f"Питомец {pet['name']} поиграл! Он заработал 10 монет")
        if a>5:
            bot.send_message(chat_id, f"Питомец {pet['name']} сделал сальто! Он заработал ещё 20 монет")

    elif message.text == "Спать":
        sleep_pet(pet)
        status_of_sleep = "спит" if pet["is_sleep"] else 'проснулся'
        bot.send_message(chat_id, f"Питомец {pet['name']} {status_of_sleep}")
    elif message.text == "Статус":
        status = (
            f'Имя: {pet["name"]}\n'
            f'Тип: {pet["type"]}\n'
            f'Голод: {pet["hunger"]:.1f}%\n'
            f'Счастье: {pet["happines"]:.1f}%\n'
            f'Энергия: {pet["energy"]:.1f}%\n'
            f'Монеты: {pet["coins"]}\n'  
            f'Состояние: {"Спит" if pet["is_sleep"] else "Бодорствует"}\n'
        )
        bot.send_message(chat_id, status)

    elif message.text == "Монеты":
        bot.send_message(chat_id, f"У тебя есть {pet['coins']} монет.")
    if pet["hunger"] > 80:
        bot.send_message(chat_id, text=f"{pet['name']} проголодался!")
    if pet["happines"] < 20:
        bot.send_message(chat_id, text=f"{pet['name']} грустит!")
    if pet["energy"] < 10:
        bot.send_message(chat_id, text=f"{pet['name']} очень устал и хочет спать!")

bot.polling()   