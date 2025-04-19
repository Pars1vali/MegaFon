import datetime
import logging, re

from Tools.scripts.fixdiv import report
from aiogram import types

char_default_status = "➖"
char_complete_opio = "✅"
char_stop_opio = "⛔"
char_attention = "❗"
char_time_status = "⌛"
char_none_report_status = "❌"

tm_user_id  = "7405295017"


opio_list = list([
    "Став 189",
    "Став 141",
    "Став/Веш",
    "Лента",
    "Оз",
    "Мачуги",
    "Игнатова",
    "Сормовская",
    "Тюляева",
    "Новомих",
    "Гулькевичи",
    "Туапсе Маркса",
    "Туапсе Жукова",
    "Кропоткин 226",
    "Кропоткин 72",
    "Усть-Лабинск Ленина",
    "Усть-Лабинск Ободовского"
])


def info():
    return """
1. /start "Название отчета"\n📄  
Создает отчет для всех ОПиО  
Ответьте на сообщение бота с фотографией 📸 и укажите название ОПиО в описании.
✅ Отчет сдан для ОПиО!\n
2. /stop "Название ОПиО"\n⛔ 
Ставит статус "на стопе" для ОПиО.\n
3. /cancel "Название ОПиО"\n➖  
Устанавливает статус по умолчанию для ОПиО.\n
4. /control
Проверяет сдачу отчетов всеми ОПиО и уведомляет ТМ
5. /help\n❓  
Инструкция по работе с ботом."""


def create(report_name: str, char_status):
    logging.info(f"Create report with name - {report_name}")
    date_now = datetime.datetime.now()
    report_message = f"{date_now.day:0>2}.{date_now.month:0>2} ️\n"
    report_message += f"{char_attention} {report_name} {char_attention}\n"
    report_message += '\n'.join([f'{opio} - {char_status}' for opio in opio_list])

    return report_message


def control(message: types.Message):
    if is_reply(message):
        report_complete = not bool(re.search(f"[{char_default_status}{char_time_status}]", message.text))
        logging.info(f"Report control. Report complete - {report_complete}")
        return report_complete


def is_reply(message: types.Message):
    if message is None:
        logging.info("Reply message is null. Need send answer for reply message.")
        return False
    return True


