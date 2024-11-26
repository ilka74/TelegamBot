"""
Многофункциональный телеграм-бот. Данный бот умеет обрабатывать фотографии и делать ASCII-арт.
Проект использует библиотеки telebot (для взаимодействия с Telegram API) и Pillow (для работы с изображениями)

Функции обработки изображений:
- resize_image: изменяет размер изображения с сохранением пропорций.
- grayify: преобразует цветное изображение в оттенки серого.
- image_to_ascii: основная функция для преобразования изображения в ASCII-арт. Изменяет размер, преобразует
в градации серого и затем в строку ASCII-символов.
- pixels_to_ascii: конвертирует пиксели изображения в градациях серого в строку ASCII-символов,
используя предопределенную строку ASCII_CHARS.
- pixelate_image: принимает изображение и размер пикселя. Уменьшает изображение до размера,
где один пиксель представляет большую область, затем увеличивает обратно, создавая пиксельный эффект.
- invert_colors: функция инверсии цветов изображения
- mirror_image: функция отражения изображения по горизонтали или вертикали
- convert_to_heatmap: функция преобразования изображения в тепловую карту


Обработчики событий:
- @bot.message_handler(commands=['start', 'help']): для текстовых команд. Реагирует на команды /start и /help,
отправляя приветственное сообщение.
- @bot.message_handler(content_types=['photo']): для получения изображений. Реагирует на изображения,
отправляемые пользователем, и предлагает варианты обработки.
- @bot.callback_query_handler: (func=lambda call: True): определяет действия в ответ на выбор пользователя
(например, пикселизация или ASCII-арт) и вызывает соответствующую функцию обработки.

Функции отправки изображений:
- pixelate_and_send: пикселизирует изображение и отправляет его обратно пользователю
- ascii_and_send: преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения
- invert_and_send: инверсия цветов
- mirror_and_send: отражение изображения
- heatmap_and_send(message): преобразование изображения в тепловую карту.

Инициализация бота:
- bot.polling(none_stop=True).

Описание импортов:
* import io: импортирует модуль io, который обеспечивает возможность работы с потоками. Он используется здесь
для обработки операций с файлами в памяти, таких как чтение и запись данных изображений;
* import os: взаимодействие с операционной системой. В данном проекте используется для получения значения
токена бота из переменной окружения;
* import telebot: импортирует библиотеку telebot, которая используется для взаимодействия с API Telegram Bot.
Позволяет создавать ботов, которые могут отправлять и получать сообщения, обрабатывать команды и многое другое;
* from PIL import Image: импортирует модуль Image из библиотеки Pillow. Этот модуль используется для открытия,
обработки и сохранения изображений в различных форматах;
* from PIL import ImageOps: импорт модуля ImageOps из библиотеки Pillow. Включает в себя различные операции,
такие как инверсия цветов, поворот и обрезка изображений и др.;
* from dotenv import load_dotenv: библиотека dotenv используется для загрузки переменных окружения из файла .env
В проекте load_dotenv вызывается для загрузки переменной TELEGRAM_BOT_TOKEN из файла .env,
чтобы обеспечить безопасность токена бота;
* from telebot import types: импортирует модуль types из библиотеки telebot, который содержит различные классы
и функции для создания различных типов объектов Telegram, таких, как клавиатуры и кнопки.
"""
import io
import os

import telebot
from PIL import Image, ImageOps
from PIL.ImageOps import grayscale
from dotenv import load_dotenv
from telebot import types
from telebot.apihelper import download_file

# Инициализация бота с использованием токена
load_dotenv()  # Загружаем переменные из .env файла
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

# Состояние пользователя хранится в словаре
user_states = {}

# Набор символов для создания ASCII-арта
ASCII_CHARS = '@%#*+=-:. '

def resize_image(image, new_width=100):
    """
    Функция изменения размера изображения
    """
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))

def grayify(image):
    """
    Преобразование изображения в градации серого
    """
    return image.convert("L")

def image_to_ascii(image_stream, new_width=40, ascii_chars=ASCII_CHARS):
    """
    Преобразование изображения в ASCII-арт
    image_stream: поток изображения
    new_width: новая ширина для изменения размера
    ascii_chars: набор символов для ASCII-арта
    """
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # меняем размер, сохраняя отношение сторон
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(
        aspect_ratio * new_width * 0.55)  # корректируем соотношение для ASCII, так как высота букв больше, чем ширина
    img_resized = image.resize((new_width, new_height))

    # Конвертируем пиксели в ASCII-символы
    img_str = pixels_to_ascii(img_resized, ascii_chars)
    img_width = img_resized.width

    # Ограничение на количество символов
    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art

def pixels_to_ascii(image, ascii_chars):
    """
    Преобразование пикселей в ASCII-символы
    """
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters

def pixelate_image(image, pixel_size):
    """
    Функция огрубления изображения
    """
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image

def invert_colors(image):
    """
    Функция инверсии цветов изображения
    """
    # Проверяем, что изображение в формате RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return ImageOps.invert(image)

def mirror_image(image, direction="horizontal"):
    """
    Функция отражения изображения по горизонтали или вертикали
    image: Объект PIL.Image
    direction: Направление отражения ("horizontal" или "vertical")
    """
    if direction == "horizontal":
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    elif direction == "vertical":
        return image.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        raise ValueError("Invalid direction. Use 'horizontal' or 'vertical'.")

def convert_to_heatmap(image):
    """
    Преобразование изображения в тепловую карту
    grayscale_image: преобразуем изображение в оттенки серого
    heatmap_image: применяем градиент от синего (холодные) к красному (теплые области)
    """
    grayscale_image = image.convert("L")
    heatmap_image = ImageOps.colorize(grayscale_image, black="blue", white="red")
    return  heatmap_image

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Обработчик команд /start и /help
    """
    bot.reply_to(message, "Пришлите мне изображение, и я предложу вам варианты!")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    """
    Обработчик получения изображения
    """
    bot.reply_to(message, "У меня есть ваша фотография! Пожалуйста, введите набор символов для ASCII-арта "
                          "(например, '@%#*+=-:. ').")
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id, 'ascii_chars': None}

@bot.message_handler(func=lambda message: message.chat.id in user_states and
                                          user_states[message.chat.id]['ascii_chars'] is None)
def set_ascii_chars(message):
    """
    Обработчик ввода пользовательского набора символов
    """
    user_states[message.chat.id]['ascii_chars'] = message.text
    bot.reply_to(message, "Спасибо! Теперь выберите, что бы Вы хотели сделать с изображением.",
                 reply_markup=get_options_keyboard())

def get_options_keyboard():
    """
    Создание клавиатуры с вариантами действий
    """
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    invert_btn = types.InlineKeyboardButton("Invert Colors", callback_data="invert")
    mirror_h_btn = types.InlineKeyboardButton("Mirror Horizontal", callback_data="mirror_horizontal")
    mirror_v_btn = types.InlineKeyboardButton("Mirror Vertical", callback_data="mirror_vertical")
    heatmap_btn = types.InlineKeyboardButton("Heatmap", callback_data="heatmap")
    keyboard.add(pixelate_btn, ascii_btn, invert_btn)
    keyboard.add(mirror_h_btn, mirror_v_btn)
    keyboard.add(heatmap_btn)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    """
    Обработчик нажатия кнопок
    """
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Пикселизация вашего изображения...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Преобразование вашего изображения в формат ASCII...")
        ascii_and_send(call.message)
    elif call.data == "invert":
        bot.answer_callback_query(call.id, "Инверсия цветов изображения...")
        invert_and_send(call.message)  # Функция инверсии цветов и отправки изображения
    elif call.data == "mirror_horizontal":
        bot.answer_callback_query(call.id, "Отражение изображения по горизонтали...")
        mirror_and_send(call.message, direction="horizontal")
    elif call.data == "mirror_vertical":
        bot.answer_callback_query(call.id, "Отражение изображения по вертикали...")
        mirror_and_send(call.message, direction="vertical")
    elif call.data == "heatmap":
        bot.answer_callback_query(call.id, "Создание тепловой карты изображения...")
        heatmap_and_send(call.message)

def pixelate_and_send(message):
    """
    Функция пикселизации и отправки изображения
    """
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

def ascii_and_send(message):
    """
    Функция преобразования изображения в ASCII-арт и отправки
    """
    photo_id = user_states[message.chat.id]['photo']

    # Используем пользовательские символы или стандартные
    ascii_chars = user_states[message.chat.id]['ascii_chars'] or ASCII_CHARS
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)

    # Передаем пользовательские символы
    ascii_art = image_to_ascii(image_stream, ascii_chars=ascii_chars)
    bot.send_message(message.chat.id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")

def invert_and_send(message):
    """
    Функция инверсии цветов и отправки изображения
    """
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Применяем инверсию цветов
    inverted_image = invert_colors(image)

    # Сохраняем результат в поток и отправляем
    output_stream = io.BytesIO()
    inverted_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

def mirror_and_send(message, direction):
    """
    Функция отражения изображения и отправки
    """
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Применяем отражение
    mirrored_image = mirror_image(image, direction)

    # Сохраняем результат в поток и отправляем
    output_stream = io.BytesIO()
    mirrored_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

def heatmap_and_send(message):
    """
    Функция преобразования изображения в тепловую карту, и его отправки
    photo_id: получаем ID фото и загружаем изображение
    """
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Применяем тепловую карту
    heatmap_image = convert_to_heatmap(image)

    # Сохраняем результат в поток и отправляем
    output_stream = io.BytesIO()
    heatmap_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)

# Запуск бота
bot.polling(none_stop=True)
