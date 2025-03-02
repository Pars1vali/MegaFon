import asyncio
import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
import report
from thefuzz import fuzz

logging.basicConfig(level=logging.INFO)

bot = Bot(token="8095263812:AAEhlt_PCB-kjoWuLXf_Wd-zZss1_gbBWjw")
dp = Dispatcher()

async def set_report_complete(opio_name: str, message: types.Message, char_status):
    for line_message in message.text.split("\n"):
        line_message_opio = line_message.split("-")[0].strip()
        if fuzz.ratio(line_message_opio.lower(), opio_name.lower()) > 90:
            report_message_text = message.text.replace(line_message, f"{line_message_opio} - {char_status}")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=report_message_text)
            logging.info(f"Edit message-report for price control. Report from {opio_name} complete.")


async def process_price_report(message: types.Message):
    has_price_photo = True if message.photo is not None else False
    opio_name = message.caption
    char_complete_opio = "✅"

    if has_price_photo:
        await set_report_complete(opio_name, message.reply_to_message, char_complete_opio)
    logging.info(f"Get message-report for price control from {opio_name}. In message has photo - {has_price_photo}.")



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    report_name = message.text.replace("/start", "").strip()
    price_report = report.create(report_name)
    await message.answer(price_report)
    logging.info(f"Create report. With name - {report_name}")

@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    char_stop = "⛔"
    opio_name = message.text.replace("/stop", "").strip()
    await set_report_complete(opio_name, message.reply_to_message, char_stop)
    logging.info(f"Set stop status for opio - {opio_name}.")

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message):
    char_cancel = ""
    opio_name = message.text.replace("/cancel", "").strip()
    await set_report_complete(opio_name, message.reply_to_message, char_cancel)
    logging.info(f"Cancel status for opio - {opio_name}.")

@dp.message(Command("control"))
async def cmd_control(message: types.Message):
    logging.info("Control message-report for TM.")

# Обработка сообщений пользователей
@dp.message()
async def reply_message(message: types.Message):
    if report.is_report_reply(message):
        await process_price_report(message)
    logging.info("Process with report")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())