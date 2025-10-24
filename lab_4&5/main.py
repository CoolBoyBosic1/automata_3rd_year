import re
import os


def generate_test_file(filename="input.txt"):
    """функція для створення тестового файлу"""
    print(f"Створюємо тестовий файл '{filename}'...")
    content = """2024 ; 15.123 ? 10 : 5 : 12 : STATION1 ? 5.000 : 80.1 : 10.5 : 8.500
2023 : -5.000 ; 11 ; 12 ; 0 ; BADCODE ; -10.000 ; 90.0 : 5.0 : -8.000
   2022 ? 20.000 : 1 : 1 : 5 : GOODCODE2   ; 10.000 ? 75.5 ? 15.1 : 15.000
1999 : 12.345 : 22 : 3 : 150 : ST789B : 2.123 : 60.0 : 20.2 : -0.123
2025: 10.000: 3: 4: 0: ABC1234: 5.000: 50.5: 8.0: 0.000
Це некоректний рядок, він буде проігнорований.
2000;5.000;15;7;3;SHORT;1.000;1.0;1.0;2.000
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content.strip())


def process_weather_data(input_file, output_file):
    """
    Обробка файлу згідно завдання 5
    """

    #регулярний вираз
    validation_regex = r'^\s*(\d{4})\s*[:;?]\s*(-?\d+\.\d{3})\s*[:;?]\s*(\d+)\s*[:;?]\s*(\d+)\s*[:;?]\s*(\d+)\s*[:;?]\s*([a-zA-Z0-9]{5,7})\s*[:;?]\s*(-?\d+\.\d{3})\s*[:;?]\s*(\d+\.\d{1})\s*[:;?]\s*(\d+\.\d{1})\s*[:;?]\s*(-?\d+\.\d{3})\s*$'

    replacement_string = r'\g<1>;\g<2>;\g<3>;\g<4>;\g<5>;\g<6>;\g<7>;\g<8>;\g<9>;\g<10>\n'

    wind_exceeded_count = 0
    total_records_count = 0

    print(f"Обробляємо '{input_file}' і пишемо в '{output_file}'...")

    try:
        with open(input_file, 'r', encoding='utf-8') as f_in, \
                open(output_file, 'w', encoding='utf-8') as f_out, \
                open("aux_stats.txt", 'w', encoding='utf-8') as f_aux:

            for line in f_in:
                match = re.match(validation_regex, line.strip())

                if match:
                    total_records_count += 1

                    wind_speed_str = match.group(9)
                    avg_temp_str = match.group(10)

                    try:
                        wind_speed = float(wind_speed_str)
                        avg_temp = float(avg_temp_str)

                        if wind_speed > 15:
                            wind_exceeded_count += 1

                        if avg_temp >= 0:
                            output_line = re.sub(validation_regex,
                                                 replacement_string,
                                                 line.strip())

                            f_out.write(output_line)

                    except ValueError:
                        print(f"Помилка конвертації числа в рядку: {line.strip()}")

                else:
                    if line.strip():
                        print(f"Рядок проігноровано (невірний формат): {line.strip()}")

            f_aux.write(f"кількість спостережень, коли сила вітру перевищувала 15: {wind_exceeded_count}\n")
            f_aux.write(f"загальна кількість записів: {total_records_count}\n")

    except FileNotFoundError:
        print(f"Помилка: Не знайдено вхідний файл '{input_file}'")
    except Exception as e:
        print(f"Сталася помилка: {e}")


if __name__ == "__main__":
    INPUT_FILENAME = "input.txt"
    OUTPUT_FILENAME = "output.txt"
    STATS_FILENAME = "aux_stats.txt"

    generate_test_file(INPUT_FILENAME)
    process_weather_data(INPUT_FILENAME, OUTPUT_FILENAME)

    print("\n--- Результат ---")
    print(f"\nОбробку завершено. Результат у файлі '{OUTPUT_FILENAME}'.")
    print(f"Статистика у файлі '{STATS_FILENAME}'.")

    print(f"\nВміст '{OUTPUT_FILENAME}':")
    try:
        with open(OUTPUT_FILENAME, 'r', encoding='utf-8') as f:
            print(f.read())

        print(f"\nВміст '{STATS_FILENAME}':")
        with open(STATS_FILENAME, 'r', encoding='utf-8') as f:
            print(f.read())
    except Exception as e:
        print(f"Не вдалося прочитати вихідні файли: {e}")
