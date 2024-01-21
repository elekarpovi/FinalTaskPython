import decimal
import logging
import argparse
"""
Банкомат. Начальная сумма 0. Допустимые действия: пополнить, снять, выйти. Сумма пополнения и 
снятия кратны 50 у.е. Комиссия за снятие 1,5% от суммы снятия, но не менее 30 у.е. и не более
600 у.е. После каждой третьей операции пополнения или снятия начисляется 3%. Нельзя снять больше, 
чем есть на счете. При превышении суммы в 5 млн. вычитать налог на богатство 10%. Любое действие 
выводит сумму денег на счете.
Добавить логирование ошибок и полезной информации. Реализовать возможность запуска из командной 
строки с передачей параметров.
"""

LOG_FILE_NAME = "terminal.log"
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler(LOG_FILE_NAME, encoding="UTF-8")
handler.setLevel(logging.INFO)
logger.addHandler(handler)

money_in_atm = decimal.Decimal()
count_operation = 0


def tax():
    global money_in_atm
    TAXFORMLN = 5_000_000
    if money_in_atm > TAXFORMLN:
        money_in_atm *= decimal.Decimal(0.9)
        print("Налог 10% при сумме больше 5 млн. у.е.")


def is_multiple_of_50(value):
    return value % 50 == 0


def count_increase():
    global count_operation
    count_operation += 1
    if not count_operation % 3:
        global money_in_atm
        money_in_atm *= decimal.Decimal(1.03)
        print("Начисление 3%")


def put_money(value):
    tax()
    global money_in_atm
    if is_multiple_of_50(value):
        money_in_atm += value
        logger.info(f"Приход: {value}")
        count_increase()
        return f"Счет пополнен на {value} у.е."
    else:
        logger.error("Можно пополнять на сумму, кратную 50")
        return "Можно пополнять на сумму, кратную 50"


def take_money(value):
    tax()
    TAXFORTAKEMONEY = 1.5
    MINTAXFORTAKEMONEY = 30
    MAXTAXFORTAKEMONEY = 600
    global money_in_atm
    if is_multiple_of_50(value):
        count_increase()
        comissia = value / 100 * TAXFORTAKEMONEY
        if money_in_atm >= value:
            money_in_atm -= value
            logger.info(f"Расход: {value}")
            if MINTAXFORTAKEMONEY <= comissia <= MAXTAXFORTAKEMONEY:
                money_in_atm -= comissia
            elif comissia < MINTAXFORTAKEMONEY:
                money_in_atm -= MINTAXFORTAKEMONEY
            else:
                money_in_atm -= MAXTAXFORTAKEMONEY
            return (f"Вы сняли {value} у.е. Комиссия за снятие {TAXFORTAKEMONEY}%, но не менее {MINTAXFORTAKEMONEY} и не более {MAXTAXFORTAKEMONEY} у.е.")
        else:
            logger.error(f"На вашем счете недостаточно средств для снятия {value}")
            return "На вашем счете недостаточно средств для снятия"
    return "Можно снять сумму, кратную 50"


def task():
    while True:
        print (f"На вашем счете {money_in_atm:.2f} у.е.")
        print("Введите от 1 до 3")
        print("1 - Пополнить счет")
        print("2 - Снять со счета")
        print("3 - Выйти")
        choice = input()
        match choice:
            case "1":
                print(put_money(int(input("Введите сумму пополнения счета: "))))
            case "2":
                print(take_money(int(input("Введите сумму снятия: "))))
            case "3":
                break
            case _:
                print("Введено неверное значение")


def out_parser():
    parser = argparse.ArgumentParser(description='My first argument parser')
    parser.add_argument('-d', '--value', nargs="*")
    return parser.parse_args()


def main():
    task()


if __name__ == '__main__':
    main()
    out = out_parser()
    
