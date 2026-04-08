import telebot
import os

TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

bot = telebot.TeleBot(TOKEN)

users = {}

@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    users[user.id] = user.username

    bot.send_message(
        message.chat.id,
        "Здравствуйте! Напишите своё сообщение.\nАдминистратор ответит вам анонимно."
    )

    username = f"@{user.username}" if user.username else "нет"

    bot.send_message(
        ADMIN_ID,
        f"📩 Новый пользователь\n\nID: {user.id}\nUsername: {username}"
    )


@bot.message_handler(commands=['reply'])
def reply(message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split(" ", 2)

    if len(parts) < 3:
        bot.send_message(ADMIN_ID, "Используй:\n/reply ID текст")
        return

    user_id = int(parts[1])
    text = parts[2]

    bot.send_message(user_id, f"✉️ Ответ администратора:\n{text}")
    bot.send_message(ADMIN_ID, "Ответ отправлен")


@bot.message_handler(func=lambda m: True)
def forward_to_admin(message):

    if message.from_user.id == ADMIN_ID:
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "нет"

    bot.send_message(
        ADMIN_ID,
        f"📨 Сообщение\n\nID: {user.id}\nUsername: {username}\n\n{message.text}"
    )

    bot.send_message(message.chat.id, "✅ Сообщение отправлено администратору")


print("Bot started")

bot.infinity_polling()
