import asyncio
import datetime
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from thefuzz import fuzz

char_complete_opio = "✅"
opio_list = {
    "Став 189": None,
    "Став 141": None,
    "Лента": None,
    "Оз": None,
    "Новомих": None,
    "Ахтарск": None,
    "Тимашевск":None,
    "Гк4": None,
    "Гк7": None,
    "Туапсе_Маркса": None,
    "Туапсе_Жукова": None,
    "Гулькевичи": None,
    "Кропоткин 226": None,
    "Кропоткин 72": None
}

def make_price_report(opio_list: dict):
    logging.info("Send message-report for price control")
    date_now = datetime.datetime.now()
    price_report = f"{date_now.day}.{date_now.month:0>2}\n"
    price_report += "Стоимостная до 11:00❗️\n"
    price_report += "\n".join(opio_list)
    return price_report

def check_is_price_report_message(message_replied_text: str):
    return True if message_replied_text.split("\n")[1].strip().split(" ")[0] == "Стоимостная" else False

async def set_report_complete(opio_name: str, message: types.Message):
    for line_message in message.text.split("\n"):
        if fuzz.ratio(line_message.lower(), opio_name.lower()) > 90:
            report_message_text = message.text.replace(line_message, f"{line_message} {char_complete_opio}")
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text=report_message_text)
            logging.info(f"Edit message-report for price control. Report from {opio_name} complete.")

async def process_price_report(message: types.Message):
    has_price_photo = True if message.photo is not None else False
    opio_name = message.caption

    if has_price_photo:
        await set_report_complete(opio_name, message.reply_to_message)
    logging.info(f"Get message-report for price control from {opio_name}. In message has photo - {has_price_photo}.")


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)
# Объект бота
bot = Bot(token="8095263812:AAEhlt_PCB-kjoWuLXf_Wd-zZss1_gbBWjw")
# Диспетчер
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    price_report = make_price_report(opio_list)
    await message.answer(price_report)

@dp.message(Command("stop"))
async def cmd_start(message: types.Message):
    pass

@dp.message(Command("cancel"))
async def cmd_start(message: types.Message):
    pass

# Обработка сообщений пользователей
@dp.message()
async def reply_message(message: types.Message):
    is_message_price_report = check_is_price_report_message(message.reply_to_message.text)
    if is_message_price_report:
        await process_price_report(message)
        logging.info("Process with price-report")


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())