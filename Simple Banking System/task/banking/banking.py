# Write your code here
import random
import sqlite3


def luna_check(sequence):
    check_sum = 0
    for i in range(len(sequence)):
        digit = int(sequence[i])
        if i % 2 == 0:
            digit *= 2
        if digit > 9:
            digit -= 9
        check_sum += digit
    return str((10 - (check_sum % 10)) % 10)


def input_choice(menu):
    display = ''
    cnt = 1
    for item in menu:
        display += f'{cnt}. {item}\n'
        cnt += 1
    display += '0. Exit\n' \
               'Enter your choice: >\n'
    return int(input(display))


def account_create(cursor):
    cursor.execute('SELECT MAX(id) FROM card;')
    max_id = cursor.fetchone()[0]
    if max_id:
        id_ = max_id + 1
    else:
        id_ = 1
    first_15 = '400000%09d' % id_
    card_id = first_15 + luna_check(first_15)
    random.seed()
    pin = '%04d' % (random.randint(1, 9999))
    cursor.execute(f'INSERT INTO card (id, number, pin) VALUES ({id_}, {card_id}, {pin});')
    conn.commit()
    print(
        'Your card has been created\n'
        'Your card number:\n'
        f'{card_id}\n'
        'Your card PIN:\n'
        f'{pin}\n'
    )
    return conn.commit()


def account_login(cursor):
    card_number_input = input('Enter your card number:\n>')
    pin_input = input('Enter your PIN:\n>')
    cursor.execute(f'SELECT pin FROM card WHERE number = {card_number_input};')
    pin_saved = cursor.fetchone()
    if pin_saved is None or pin_input != pin_saved[0]:
        print('Wrong card number or PIN!')
    else:
        print('You have successfully logged in!')
        return card_number_input


def get_balance(cursor, card_id):
    cursor.execute(f'SELECT balance FROM card WHERE number = {card_id};')
    balance = cursor.fetchone()[0]
    print(balance)


def add_income(cursor, card_id):
    cursor.execute(f'SELECT balance FROM card WHERE number = {card_id};')
    balance = cursor.fetchone()[0] + int(input('\nEnter income:\n'))
    cursor.execute(f'UPDATE card SET balance = {balance} WHERE number = {card_id};')
    print('Income was added!\n')
    return conn.commit()


def do_transfer(cursor, card_id):
    transfer_id = input('Transfer\n'
                        'Enter card number\n')
    cursor.execute(f'SELECT number, balance FROM card WHERE number = {transfer_id};')
    transfer_check = cursor.fetchone()
    if transfer_id[-1] != luna_check(transfer_id[:-1]):   # perform luna_check to transfer_id
        print('Probably you made a mistake in the card number. Please try again!')

    elif transfer_check is None:
        print('Such a card does not exist.')

    elif transfer_check[0] == transfer_id:  # perform check if transfer_id exists
        request = int(input('Enter how much money you want to transfer:\n'))
        cursor.execute(f'SELECT balance FROM card WHERE number = {card_id};')
        balance_from = cursor.fetchone()[0]
        if request > balance_from:
            print('Not enough money!\n')
        else:
            balance_from -= request
            balance_to = transfer_check[1] + request
            cursor.execute(f'UPDATE card SET balance = {balance_from} WHERE number = {card_id};')
            cursor.execute(f'UPDATE card SET balance = {balance_to} WHERE number = {transfer_id};')
            print('Success!\n')
            return conn.commit()
    else:
        print('Such a card does not exist.')


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute(
    '''CREATE TABLE IF NOT EXISTS card (
    id INTEGER,
    number TEXT,
    pin TEXT,
    balance INTEGER DEFAULT 0);'''
)
conn.commit()

start_menu = ['Create an account', 'Log in']
account_menu = ['Balance', 'Add income', 'Do transfer', 'Close account', 'Log out']

while True:
    start_choice = input_choice(start_menu)
    if start_choice == 1:
        account_create(cur)
        conn.commit()
    elif start_choice == 2:
        card_number = account_login(cur)
        if card_number is None:
            continue
        #  print(card_number)
        while True:
            account_choice = input_choice(account_menu)
            if account_choice == 1:
                get_balance(cur, card_number)
            elif account_choice == 2:
                add_income(cur, card_number)
            elif account_choice == 3:
                do_transfer(cur,card_number)
            elif account_choice == 4:
                cur.execute(f'DELETE FROM card WHERE number = {card_number};')
                conn.commit()
                print('The account has been closed!')
                break
            elif account_choice == 5:
                break
            elif account_choice == 0:
                print('Bye!')
                exit()
    elif start_choice == 0:
        break

    else:
        print('You have made wrong choice.\nPlease try again.\n')
        continue
print('Bye!')
