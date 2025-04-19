import logging
import json, os, re
import report
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import F
from thefuzz import process


logging.getLogger().setLevel(logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


async def set_report_complete(opio_name: str, message: types.Message, char_status):
    if report.is_reply(message):
        opio, probability = process.extract(opio_name, report.opio_list, limit=1)[0]
        report_message = re.sub(f'{opio} - [{report.char_complete_opio}{report.char_time_status}{report.char_default_status}{report.char_stop_opio}]', \
                                f"{opio} - {char_status}", \
                                message.text)
        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                    text=report_message)
        logging.info(f"Edit message-report. Report from {opio} complete. Set status - {char_status}")


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    report_name = message.text.replace("/start", "").strip()
    price_report = report.create(report_name, report.char_default_status)
    await message.answer(price_report)
    logging.info(f"Create report. With name - {report_name}, chat_id - {message.chat.id}")


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
    has_price_photo = True if message.photo is not None else False
    if has_price_photo:
        opio_name = message.caption.replace("/report", "").strip()
        await set_report_complete(opio_name, message.reply_to_message, report.char_complete_opio)
        logging.info(f"Get message-report for price control from {opio_name}. In message has photo - {has_price_photo}.")


@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(report.info())
    logging.info("Send instructions for uses bot and avalible command.")


@dp.message(Command("delete"))
async def cmd_delete(message: types.Message):
    if report.is_reply(message.reply_to_message):
        report_message = message.reply_to_message
        is_delete = await bot.delete_message(report_message.chat.id, report_message.message_id)
        logging.info(f"Report delete - {is_delete}")


@dp.message(Command("copy"))
async def cmd_copy(message: types.Message):
    if report.is_reply(message.reply_to_message):
        await message.answer(message.reply_to_message.text)
        logging.info(f"Copy report message")


@dp.message(Command("control"))
async def cmd_control(message: types.Message):
    if report.control(message.reply_to_message):
        await message.answer(f'{message.reply_to_message.text}\nОтчёт сдан. [Александра ТМ](tg://user?id={report.tm_user_id})', \
                             parse_mode="Markdown")
        logging.info(f"Control message-report. Report complete.")
    else:
        await message.answer('Отчёт не сдан.')
        logging.info(f"Control message-report. The report has not been submitted")

@dp.message(Command("test"))
async def test(message: types.Message):
    price_report = report.create("Отчет о продажах", report.char_none_report_status)
    report_message = await message.answer(text=price_report)

    type_report = "day_sales"
    message_id = report_message.message_id
    message_date = report_message.date
    chat_id = report_message.chat.id
    chat_type = report_message.chat.type

    builder = InlineKeyboardBuilder()
    builder.row(
        types.InlineKeyboardButton(
            text="Загрузить",
            url=f"https://daily-report-megafon.streamlit.app/?type_report={type_report}&message_id={message_id}&message_date={message_date}&chat_id={chat_id}&chat_type={chat_type}"
        )
    )

    await message.answer("Отчет о продажах", reply_markup=builder.as_markup())

async def handler(event, context):
    update = json.loads(event['body'])
    update = types.Update.parse_obj(update)
    try:
        await dp.feed_update(bot, update)
    except Exception as e:
        logging.error(f"Error - {e}.")

    return {
        'statusCode': 200,
        'body': 'Bot automatic report complete',
    }