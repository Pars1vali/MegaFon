import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
import report
from thefuzz import fuzz
from thefuzz import process
import json, os, re

from report import is_reply

logging.getLogger().setLevel(logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_report_complete(opio_name: str, message: types.Message, char_status):
    if report.is_reply(message):
        opio, probability = process.extract(opio_name, report.opio_list, limit=1)[0]
        report_message = re.sub(f'{opio} - [{report.char_time_status}{report.char_default_status}{report.char_stop_opio}]', \
                                f"{opio} - {char_status}", \
                                message.text)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                    text=report_message)
        logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")



@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    report_name = message.text.replace("/start", "").strip()
    report_message = report.create(report_name)
    await message.answer(report_message)
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


@dp.message(Command("report"))
async def cmd_report(message: types.Message):
    has_photo = True if message.photo is not None else False
    if has_photo:
        opio_name = message.caption.replace("/report", "").strip()
        await set_report_complete(opio_name, message.reply_to_message, report.char_complete_opio)
        logging.info(f"Get message-report for price control from {opio_name}. In message has photo - {has_photo}.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(report.info())
    logging.info("Send instructions for uses bot and avalible command.")


@dp.message(Command("control"))
async def cmd_control(message: types.Message):
    if report.control(message.reply_to_message):
        await message.answer(f'{message.reply_to_message.text} \n Отчёт сдан. [{message.from_user.first_name}](tg://user?id={message.from_user.id})', \
                             parse_mode="Markdown")
        logging.info(f"Control message-report. Report complete.")
    else:
        await message.answer('Отчёт не сдан.')
        logging.info(f"Control message-report. The report has not been submitted")



# Обработка сообщений пользователей
# @dp.message()
# async def reply_message(message: types.Message):
#     if report.is_report_reply(message.reply_to_message):
#         await process_price_report(message)
#     logging.info("Process with report")

async def handler(event, context):
    update = json.loads(event['body'])
    update = types.Update.parse_obj(update)
    try:
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(f"Error - {e}.\n Stacktrace - {e.with_traceback()}")

    return {
        'statusCode': 200,
        'body': 'Bot automatic report complete',
    }