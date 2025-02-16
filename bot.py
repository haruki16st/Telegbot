import telebot
from telebot import types
import os
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

# Получаем токен и ID админа из окружения
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")
MENTOR_USERNAME = "haruki16st"  # твой ник

bot = telebot.TeleBot(TOKEN)

users = {}

# Старт команды
@bot.message_handler(commands=['start'])
def start_message(message):
    chat_id = message.chat.id
    users[chat_id] = {}
    bot.send_message(
        chat_id,
        "👋 Добро пожаловать в *16ST FAMILY!* 🚀\n\n"
        "Чтобы стать частью нашей команды, заполни анкету 👇\n\n"
        "📌 *1) Откуда вы узнали о нас?*",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_question_1)

# Вопрос 1
def process_question_1(message):
    chat_id = message.chat.id
    users[chat_id]['source'] = message.text
    bot.send_message(
        chat_id,
        "🛠 *2) Имеется ли у Вас опыт работы в данной сфере?*",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_question_2)

# Вопрос 2
def process_question_2(message):
    chat_id = message.chat.id
    users[chat_id]['experience'] = message.text
    bot.send_message(
        chat_id,
        "⏳ *3) Сколько времени Вы готовы уделять работе и какого результата хотите добиться?*",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, process_question_3)

# Финальный шаг — отправка админу
def process_question_3(message):
    chat_id = message.chat.id
    users[chat_id]['goals'] = message.text

    application = (
        f"📝 *Новая заявка в 16ST FAMILY!*\n\n"
        f"👤 *Отправитель:* @{message.from_user.username}\n"
        f"📌 *Источник:* {users[chat_id]['source']}\n"
        f"🛠 *Опыт:* {users[chat_id]['experience']}\n"
        f"⏳ *Время и цели:* {users[chat_id]['goals']}\n\n"
        f"⚡ *Принять или отклонить заявку?*"
    )

    # Отправляем админу
    keyboard = types.InlineKeyboardMarkup()
    accept_button = types.InlineKeyboardButton("✅ Принять", callback_data=f"accept_{chat_id}")
    reject_button = types.InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{chat_id}")
    keyboard.add(accept_button, reject_button)

    bot.send_message(ADMIN_CHAT_ID, application, parse_mode="Markdown", reply_markup=keyboard)
    bot.send_message(chat_id, "📨 *Ваша заявка отправлена!* Ожидайте решения администратора.", parse_mode="Markdown")

# Обработчик нажатий (Принять/Отклонить)
@bot.callback_query_handler(func=lambda call: call.data.startswith("accept_") or call.data.startswith("reject_"))
def handle_callback(call):
    chat_id = int(call.data.split("_")[1])

    if call.data.startswith("accept"):
        # Отправка уведомления пользователю, если его заявку приняли
        bot.send_message(
            chat_id,
            "🎉 *Поздравляем!* Ваша заявка в *16ST FAMILY* принята! 🚀\n\n"
            "🔥 *Теперь ты часть нашей команды!* 🔥\n"
            "🔹 Будь активным, помогай другим и достигай новых высот.\n\n"
            f"👨‍🏫 *Твой наставник:* @{MENTOR_USERNAME}\n"
            f"✉️ *Напиши ему в Telegram:* [Связаться](https://t.me/{MENTOR_USERNAME})\n\n"
            "📌 Чтобы вступить в команду, напиши своему наставнику.",
            parse_mode="Markdown"
        )

        # Добавление кнопки "Выбрать наставника"
        keyboard = types.InlineKeyboardMarkup()
        mentor_button = types.InlineKeyboardButton("Выбрать наставника", url=f"https://t.me/{MENTOR_USERNAME}")
        keyboard.add(mentor_button)
        bot.send_message(chat_id, "Нажми на кнопку ниже, чтобы выбрать наставника и вступить в команду!", reply_markup=keyboard)

        # Уведомление администратора
        bot.send_message(ADMIN_CHAT_ID, f"✅ @{MENTOR_USERNAME} принял нового участника: @{bot.get_chat(chat_id).username}")

    else:
        bot.send_message(chat_id, "❌ *К сожалению, ваша заявка отклонена.* Вы можете попробовать снова позже.", parse_mode="Markdown")
        bot.send_message(ADMIN_CHAT_ID, f"❌ Админ отклонил заявку @{bot.get_chat(chat_id).username}")

# Правила для чата
@bot.message_handler(commands=['rules'])
def send_rules(message):
    rules = (
        "📜 *Правила 16ST FAMILY:*\n\n"
        "1️⃣ Уважай участников и администрацию.\n"
        "2️⃣ Запрещена реклама и спам.\n"
        "3️⃣ Не распространяй ложную информацию.\n"
        "4️⃣ Соблюдай правила сообщества.\n"
        "5️⃣ Помни: Мы одна команда! 🤝"
    )
    bot.send_message(message.chat.id, rules, parse_mode="Markdown")

# Запуск бота
bot.polling(none_stop=True)
