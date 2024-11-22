import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, InlineQueryResultArticle, InputTextMessageContent
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.client.bot import DefaultBotProperties
import asyncio
import json
import settings
from datetime import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=settings.API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))

dp = Dispatcher()

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    webAppInfo = WebAppInfo(url="https://blumticket.web.app")
    inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Сообщить о проблеме', web_app=webAppInfo)]])
    await message.answer(
        text=f"Добро пожаловать {message.from_user.first_name}, это бот регистрации проблемы в приложении Blum, нажмите кнопку \"Сообщить о проблеме\", чтобы открыть форму и зарегистрировать проблему..",
        reply_markup=inline_keyboard
    )
    await bot.send_message(chat_id=settings.botadmin, text=f"[{message.from_user.first_name}](tg://user?id={message.from_user.id}) нажал Start")

@dp.message(F.web_app_data)
async def handle_webapp_data(message: types.Message):
    print("========== Web App Data received =============")
    data = json.loads(message.web_app_data.data)
    query_id = data['query_id']
    problemshort = data["problemshort"]
    waitresult = data["waitresult"]
    actualresult = data["actualresult"]
    problemdescription = data["problemdescription"]
    categoryselection = data["categoryselection"]
    blumname = data["blumname"]
    device = data["device"]
    osversion = data["osversion"]
    location = data["location"]
    user_id = data["user_id"]
    username = data["username"]
    first_name = data["first_name"]
    current_date_time = datetime.now()
    current_time = current_date_time.strftime("%d-%m-%Y %H:%M")

    answer_text = (f"*• ShortDesc:* `{problemshort}`\n"
                   f"*• Expected :* `{waitresult}`\n"
                   f"*• Actual:* `{actualresult}`\n"
                   f"*• Description:* `{problemdescription}`\n"
                   f"*• Category:* `{categoryselection}`\n"
                   f"*• Blum Name:* `{blumname}`\n"
                   f"*• Device:* `{device}`\n"
                   f"*• OS Version:* `{osversion}`\n"
                   f"*• Location:* `{location}`\n"
                   f"=================\n"
                   f"*• UserID:* `{user_id}`\n"
                   f"*• TGUsername:* `@{username}`\n"
                   f"*• Name:* `{first_name}`\n"
                   f"=================\n"
                   f"*• TicketID:* `{query_id}`\n"
                   f"*• Date:* {current_time} GMT +5")

    # Использование метода answerWebAppQuery для отправки сообщения от имени пользователя
    await bot.answer_web_app_query(
            web_app_query_id=query_id,
            result=InlineQueryResultArticle(
                id=query_id,
                title="Ваши данные",
                input_message_content=InputTextMessageContent(message_text=answer_text)
            ))
    try:
        await bot.send_message(chat_id=settings.info_channel, text=answer_text)
    except Exception as e:
        print(e)

ALLOWED_UPDATES = ["message", "web_app_data", "inline_query", "web_app_query_id"]


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)

asyncio.run(main())

