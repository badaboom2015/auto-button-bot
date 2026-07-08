import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "8875131920:AAE9dyMAYVGgOjYCd6faK_fvQSodG6CDwM8"
CHANNEL = "@AutoBuyNow"
ADMIN_CHAT_ID = 6797548910

PINNED_TEXT = """📌 Добро пожаловать в наш авто-канал! 🚘￼

Здесь вы найдёте всё, что связано с автомобилями: покупка, продажа, автоподбор, ремонт, инвестиции и многое другое!

Наши услуги:

🔧 СТО-услуги – маляр, механик, электрик, диагностика, ремонт авто под ключ 🔑

🇩🇪 Немецкий Copart – автоподбор автомобилей на любой вкус 🏎️

🚛 Манипулятор – услуги по всей Европе 🇪🇺

💰 Инвестиции – принимаем инвестиции официально по договору 🤝🏻30% годовых | Выплаты каждый месяц 
👉@johannescar 

📍Андрес: 
  Gerbrunn,
  Alte Landstraße 1d,
  97218

📍Google Maps
☎️+49 176 21680224


Хотите продать свой автомобиль? 🚗💰

📢 Разместить объявление в нашем канале можно бесплатно!🆓 

Для этого свяжитесь с нашим менеджером 👉@johannescar 

💬 Повторное размещение объявления – по договорённости с менеджером.

Instagram: https://www.instagram.com/johannes.wuerzburg?igsh=b3RueTdlejBtbjkx&utm_source=qr

TikTok: 
www.tiktok.com/@johannes.global

🔥 Продавайте и покупайте авто легко и быстро вместе с нами! 🔥"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""👋 Здравствуйте!

Для бесплатной публикации отправьте одним сообщением:

🚗 Марка и модель
📅 Год выпуска
🛣 Пробег
⚙️ Двигатель / КПП
💶 Цена
📍 Город
📝 Краткое описание
📸 Фотографии автомобиля
☎️ Контакт для связи

После проверки менеджером объявление будет опубликовано в канале.""")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.forward(chat_id=ADMIN_CHAT_ID)
    await update.message.reply_text("✅ Спасибо! Ваше объявление получено.")

async def post_pinned_message():
    bot = Bot(token=TOKEN)
    me = await bot.get_me()

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚗 ПРОДАТЬ АВТО", url=f"https://t.me/{me.username}?start=sellcar")]
    ])

    msg = await bot.send_message(
        chat_id=CHANNEL,
        text=PINNED_TEXT,
        reply_markup=keyboard,
        disable_web_page_preview=True
    )

    await bot.pin_chat_message(
        chat_id=CHANNEL,
        message_id=msg.message_id,
        disable_notification=True
    )

def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(post_pinned_message())

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO | filters.Document.ALL, forward_to_admin))

    app.run_polling()

if __name__ == "__main__":
    main()
