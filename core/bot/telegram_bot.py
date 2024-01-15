import os
from json import JSONDecodeError

import requests
from django.conf import settings
import telebot
from telebot import types
from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(os.environ["TELEGRAM_TOKEN"])
api_url = os.environ["API_URL"]

telebot.logger.setLevel(settings.LOG_LEVEL)


@bot.message_handler(commands=['help', 'start'])
async def send_welcome(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton(text="Узнать погоду")
    keyboard.add(button)

    await bot.reply_to(message, """\
Здравствуйте, я бот, который может предоставить данные о погоде в нужном городе.
Для получения информации о погоде, нажмите кнопку "Узнать погоду".""",
                       reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Узнать погоду')
async def handle_weather_request(message):
    await bot.send_message(message.chat.id, "Введите название города:")


@bot.message_handler(func=lambda message: True)
async def handle_text(message):
    city_name = message.text.capitalize()
    weather_data = get_weather_data(city_name)

    if not weather_data:
        return await bot.send_message(
            message.chat.id,
            "К сожалению, данный город не найден. Проверьте корректность названия города!"
        )

    temperature = weather_data.get("temperature", "н/д")
    pressure = weather_data.get("pressure", "н/д")
    wind_speed = weather_data.get("wind_speed", "н/д")

    await bot.send_message(
        message.chat.id,
        f"В городе {city_name} на данный момент:"
        f"""\n\nТемпература: {temperature} °C"""
        f"""\nДавление: {pressure} мм рт. ст."""
        f"""\nСкорость ветра: {wind_speed} м/с."""
    )


def get_weather_data(city_name):
    try:
        response = requests.get(f"{api_url}weather?city={city_name}")

        if not response.ok:
            return None

        weather_data = response.json()
        return weather_data

    except JSONDecodeError:
        return None
