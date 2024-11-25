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
## Структура программы

### Функции обработки изображений:
- resize_image: изменяет размер изображения с сохранением пропорций.
- grayify: преобразует цветное изображение в оттенки серого.
- image_to_ascii: основная функция для преобразования изображения в ASCII-арт. Изменяет размер, преобразует в градации серого и затем в строку ASCII-символов.
- pixels_to_ascii: конвертирует пиксели изображения в градациях серого в строку ASCII-символов, используя предопределенную строку ASCII_CHARS.
- pixelate_image: принимает изображение и размер пикселя. Уменьшает изображение до размера, где один пиксель представляет большую область, затем увеличивает обратно, создавая пиксельный эффект.
- invert_colors: функция инверсии цветов изображения
- mirror_image: функция отражения изображения по горизонтали или вертикали


### Обработчики событий:
- @bot.message_handler(commands=['start', 'help']): для текстовых команд. Реагирует на команды /start и /help, отправляя приветственное сообщение.
- @bot.message_handler(content_types=['photo']): для получения изображений. Реагирует на изображения, отправляемые пользователем, и предлагает варианты обработки.
- @bot.callback_query_handler: (func=lambda call: True): определяет действия в ответ на выбор пользователя (например, пикселизация или ASCII-арт) и вызывает соответствующую функцию обработки. 


### Функции отправки изображений:
- pixelate_and_send: пикселизирует изображение и отправляет его обратно пользователю
- ascii_and_send: преобразует изображение в ASCII-арт и отправляет результат в виде текстового сообщения
- invert_and_send: функция инверсии цветов и отправки изображения
- mirror_and_send: функция отражения изображения и отправки


### Инициализация бота:
- bot.polling(none_stop=True).


--------------
### Скриншоты работы программы:
#### Запуск телеграмм-бота
<img src="images/img_1.PNG" alt="Запуск бота" width="600">

#### Запрос изображения от пользователя
<img src="images/img_2.PNG" alt="Запрос изображения от пользователя" width="600">

#### Изображение загружено
<img src="images/img_3.PNG" alt="Подготовка фото к обработке" width="600">

#### Запрос способа обработки изображения 
(пикселизация, преобразование в ASCII-арт, инверсия, отражение по горизонтали или вертикали)

<img src="images/img_4.PNG" alt="Запрос способа обработки изображения" width="600">

#### Пример пикселизации
<img src="images/img_5.PNG" alt="Результат пикселизации" width="600">

#### Пример преобразования того же объекта в ASCII-арт
<img src="images/img_6.PNG" alt="Результат преобразования того же изображения в ASCII-арт" width="600">

#### Пример инверсии (создание "негатива" изображения)
<img src="images/img_7.PNG" alt="Результат инверсии" width="600">

#### Пример отражения по горизонтали 
<img src="images/img_8.PNG" alt="Отражение по горизонтали" width="600">

#### Пример отражения по вертикали 
<img src="images/img_9.PNG" alt="Отражение по вертикали" width="600">
