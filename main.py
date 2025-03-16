import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
import report
from thefuzz import fuzz

logging.basicConfig(level=logging.WARNING)

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

    if has_price_photo:
        await set_report_complete(opio_name, message.reply_to_message, report.char_complete_opio)
    logging.info(f"Get message-report for price control from {opio_name}. In message has photo - {has_price_photo}.")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    report_name = message.text.replace("/start", "").strip()
    price_report = report.create(report_name)
    await message.answer(price_report)
    logging.info(f"Create report. With name - {report_name}")

@dp.message(Command("stop"))
async def cmd_stop(message: types.Message):
    opio_name = message.text.replace("/stop", "").strip()
    await set_report_complete(opio_name, message.reply_to_message, report.char_stop_opio)
    logging.info(f"Set stop status for opio - {opio_name}.")

@dp.message(Command("cancel"))
async def cmd_cancel(message: types.Message):
    opio_name = message.text.replace("/cancel", "").strip()
    await set_report_complete(opio_name, message.reply_to_message, report.char_default_status)
    logging.info(f"Cancel status for opio - {opio_name}.")


@dp.message(Command("time"))
async def cmd_time(message: types.Message):
    opio_name = message.text.replace("/time", "").strip()
    await set_report_complete(opio_name, message.reply_to_message, report.char_time_status)
    logging.info(f"Time status for opio - {opio_name}.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(report.info())
    logging.info("Send instructions for uses bot and avalible command.")


@dp.message(Command("control"))
async def cmd_control(message: types.Message):
    report_status = report.control(message.reply_to_message)
    if report_status is True:
        await message.answer(message.reply_to_message.text)
        await message.answer("Отчёт сдан.")
        # user_name = message.from_user.first_name
        # mention = "[" + user_name + "](tg://user?id=" + str(report.tm_user_id) + ")"
        # await message.answer(mention, parse_mode="Markdown")
    logging.info(f"Control message-report for TM. Report complete - {report_status}.")

# Обработка сообщений пользователей
@dp.message()
async def reply_message(message: types.Message):
    if report.is_report_reply(message.reply_to_message):
        await process_price_report(message)
    logging.info("Process with report")

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())