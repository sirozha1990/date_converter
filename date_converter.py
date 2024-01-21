import datetime
import re
import argparse
import logging

# Установка уровня логирования и настройка вывода в файл
logging.basicConfig(filename='date_converter.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_date(input_text):
    try:
        match = re.match(r'(\d+)?-?(й|я)?\s?(\w+|\d+)?\s?(\w+|\d+)?', input_text)
        if match:
            week_number = int(match.group(1)) if match.group(1) else 1
            day_of_week = match.group(3) if match.group(3) else datetime.datetime.now().isoweekday()
            month = match.group(4) if match.group(4) else datetime.datetime.now().month

            if month.isdigit():
                month = int(month)
            else:
                month_mapping = {"января": 1, "февраля": 2, "марта": 3, "апреля": 4, "мая": 5, "июня": 6, "июля": 7, "августа": 8, "сентября": 9, "октября": 10, "ноября": 11, "декабря": 12}
                month = month_mapping[month]

            if day_of_week.isdigit():
                day_of_week = int(day_of_week)
            else:
                day_of_week_mapping = {"понедельник": 1, "вторник": 2, "среда": 3, "четверг": 4, "пятница": 5, "суббота": 6, "воскресенье": 7}
                day_of_week = day_of_week_mapping[day_of_week.lower()]

            current_year = datetime.datetime.now().year
            d = datetime.date(current_year, month, 1)
            offset = (day_of_week - d.isoweekday() + 7) % 7
            date = d + datetime.timedelta(days=offset + 7 * (week_number - 1))
            logging.info(f"Результат: {date}")
            return date
        else:
            raise ValueError("Неверный формат входной строки")
    except Exception as e:
        logging.error(f"Ошибка: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Преобразование текстового описания даты в дату')
    parser.add_argument('input_text', nargs='*', help='Текстовое описание даты в формате "1-й четверг ноября"')

    args = parser.parse_args()
    if args.input_text:
        input_text = " ".join(args.input_text)
        result_date = parse_date(input_text)
        if result_date:
            print(f"Результат: {result_date}")
        else:
            logging.error("Ошибка при разборе входных данных")
            print("Ошибка при разборе входных данных. Проверьте лог для дополнительной информации.")
    else:
        logging.error("Неверный формат входных данных")
        print("Неверный формат входных данных")

if __name__ == "__main__":
    main()
