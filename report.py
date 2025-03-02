import datetime
import logging
from aiogram import types

char_default_status = "➖"
opio_list = list([
    "Став 189",
    "Став 141",
    "Лента",
    "Оз",
    "Новомих",
    "Ахтарск",
    "Тимашевск",
    "Гк4",
    "Гк7",
    "Туапсе_Маркса",
    "Туапсе_Жукова",
    "Гулькевичи",
    "Кропоткин 226",
    "Кропоткин 72"])

def create(report_name: str):
    date_now = datetime.datetime.now()
    price_report = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    price_report += F"❗{report_name}❗\n"
    price_report += '\n'.join([f'{opio} - {char_default_status}' for opio in opio_list])

    return price_report


def is_report_reply(message: types.Message):
    if message is None:
        logging.info("Reply message is null. Need send answer for reply message.")
        return False
    return True

def is_price_report(message: types.Message):
    if message is None:
        logging.info("Reply message is null. Need send answer for reply message.")
        return False
    return True if message.text.split("\n")[1].strip().split(" ")[0] == "Стоимостная" else False


