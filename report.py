import datetime
import logging
from aiogram import types

char_default_status = "➖"
char_complete_opio = "✅"
char_stop_opio = "⛔"
char_attention = "❗"

tm_user_id  = "982144139"


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


def info():
    return ("/start \"Название отчета\" - создает отчёт для ОПиО из внутреннего списка.\n"
            "Ответ на сообщение бота + фотография + название ОПиО в описании -> Отчет сдан для ОПиО\n"
            "/stop \"Название ОПиО\" - ставит статус на стопе для ОПиО.\n"
            "/cancel \"Название ОПиО\" - устанавливает статус по умолчанию для ОПиО.\n"
            "/help - Инструкция работы бота")

def create(report_name: str):
    logging.info(f"Create report with name - {report_name}")
    date_now = datetime.datetime.now()
    price_report = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    price_report += F"{char_attention} {report_name} {char_attention}\n"
    price_report += '\n'.join([f'{opio} - {char_default_status}' for opio in opio_list])

    return price_report

def control(message: types.Message):
    report_complete = True
    opio_status_list = message.text.split(char_attention)[-1].split("\n")
    for line in opio_status_list:
        status_report = line.split("-")[-1].strip()
        if status_report == char_default_status:
            report_complete = False

    return report_complete

def is_report_reply(message: types.Message):
    if message is None:
        logging.info("Reply message is null. Need send answer for reply message.")
        return False
    return True


