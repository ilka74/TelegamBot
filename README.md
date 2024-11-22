Многофункциональный телеграм-бот. Данный бот сейчас умеет работать с фотографиями и делать ASCII-арт 
=====================================================================================
## Проект использует библиотеки telebot (для взаимодействия с Telegram API) и Pillow (для работы с изображениями) 

### Импорты и настройки:
* import telebot: импортирует библиотеку telebot, которая используется для взаимодействия с API Telegram Bot. 
Позволяет создавать ботов, которые могут отправлять и получать сообщения, обрабатывать команды и многое другое;
* from PIL import Image: импортирует модуль Image из библиотеки Pillow. Этот модуль используется для открытия, 
обработки и сохранения изображений в различных форматах;
* import io: импортирует модуль io, который обеспечивает возможность работы с потоками. Он используется здесь 
для обработки операций с файлами в памяти, таких как чтение и запись данных изображений;
* from telebot import types: импортирует модуль  types из библиотеки telebot, который содержит различные классы 
и функции для создания различных типов объектов Telegram, таких как клавиатуры и кнопки.

------------
## Описание функционала

### Хранение состояний пользователей:
- user_states используется для отслеживания действий или состояний пользователей. Например, какое изображение было отправлено.

### Пикселизация
pixelate_image(image, pixel_size): принимает изображение и размер пикселя. Уменьшает изображение до размера, где один пиксель представляет большую область, затем увеличивает обратно, создавая пиксельный эффект.

### Преобразование в ASCII-арт. Подготовка изображения:
- resize_image(image, new_width=100): изменяет размер изображения с сохранением пропорций.
- grayify(image): преобразует цветное изображение в оттенки серого.
- image_to_ascii(image_stream, new_width=40): основная функция для преобразования изображения в ASCII-арт. Изменяет размер, преобразует в градации серого и затем в строку ASCII-символов.
- pixels_to_ascii(image): конвертирует пиксели изображения в градациях серого в строку ASCII-символов, используя предопределенную строку ASCII_CHARS.

### Инверсия цветов изображения:
- invert_colors(image): функция инверсии цветов изображения
- invert_and_send(message): Функция инверсии цветов и отправки изображения

### Взаимодействие с пользователем: 
Обработчики сообщений:
- @bot.message_handler(commands=['start', 'help']): реагирует на команды /start и /help, отправляя приветственное сообщение.
- @bot.message_handler(content_types=['photo']): реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки.

Клавиатура для взаимодействия:
- get_options_keyboard(): создает клавиатуру с кнопками для выбора пользователем, как обработать изображение: через пикселизацию или преобразование в ASCII-арт.

Обработка запросов. Обработка колбэков:
- @bot.callback_query_handler(func=lambda call: True): определяет действия в ответ на выбор пользователя (например, пикселизация или ASCII-арт) и вызывает соответствующую функцию обработки.

Отправка результатов. Функции отправки:
- pixelate_and_send(message): пикселизирует изображение и отправляет его обратно пользователю.
- ascii_and_send(message): преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения.

--------------
### Скриншоты работы программы:
#### Запуск телеграмм-бота
<img src="images/img_1.PNG" alt="Запуск бота" width="600">

#### Запрос изображения от пользователя
<img src="images/img_2.PNG" alt="Запрос изображения от пользователя" width="600">

#### Изображение загружено
<img src="images/img_3.PNG" alt="Подготовка фото к обработке" width="600">

#### Запрос способа обработки изображения 
(пикселизация, преобразование в ASCII-арт или инверсия)

<img src="images/img_4.PNG" alt="Запрос способа обработки изображения" width="600">

#### Пример пикселизации
<img src="images/img_5.PNG" alt="Результат пикселизации" width="600">

#### Пример преобразования того же объекта в ASCII-арт
<img src="images/img_6.PNG" alt="Результат преобразования того же изображения в ASCII-арт" width="600">

#### Пример инверсии (создание "негатива" изображения)
<img src="images/img_7.PNG" alt="Результат инверсии" width="600">
