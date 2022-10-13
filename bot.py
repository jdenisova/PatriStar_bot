import telebot
import requests
from requests.exceptions import HTTPError
import config

bot = telebot.TeleBot(config.TOKEN)


def reply_keyboard(*buttons: str, resize_keyboard=True, row_width=1):
    markup = telebot.types.ReplyKeyboardMarkup(
        resize_keyboard=resize_keyboard,
        row_width=row_width
    )
    return markup.add(*[telebot.types.KeyboardButton(button)
                        for button in buttons])


def get_image_from_api() -> (str, str):
    try:
        response = requests.get(
            "https://api.nasa.gov/planetary/apod?api_key=" + config.KEY_API
        )
        response.raise_for_status()

        image = response.json()["url"]
        explanation = response.json()["explanation"]

    except HTTPError as err:
        print(f'HTTP error: {err}')

    except KeyError as err:
        print(f"Key error: {err}")

    else:
        return image, explanation


@bot.message_handler(commands=['start', 'help'])
def start(message):
    title = "Each day a different image or photograph of our fascinating " \
            "universe is featured, along with a brief " \
            "explanation written by a professional astronomer.\n\n"\
            "Click on button to get astronomy picture of the day."

    bot.send_message(
        message.chat.id, title,
        reply_markup=reply_keyboard("Astronomy Picture of the Day")
    )


@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "Astronomy Picture of the Day":
        bot.send_message(
            message.chat.id,
            "I'm taking the photo and writing the text ..."
        )
        response = get_image_from_api()

        if response:
            image, explanation = get_image_from_api()

            bot.send_photo(message.chat.id, image)
            bot.send_message(
                message.chat.id, explanation,
                reply_markup=reply_keyboard("Astronomy Picture of the Day")
            )
        else:
            bot.send_message(
                message.chat.id,
                "Astronauts on vacation, repeat your request later.",
                reply_markup=reply_keyboard("Astronomy Picture of the Day")
            )


if __name__ == "__main__":
    bot.polling(none_stop=True)
