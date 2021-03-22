import random
import sqlite3


class Bank:
    def __init__(self):
        # 0 - main menu, 2 - Log into account
        self.state = 0
        self.accounts = {}
        self.amount_of_users = 0
        self.print_massage()
        self.current_card_number = 0
        self.second_card_number = 0
        self.current_pin = 0
        self.connection = sqlite3.connect("card.s3db")
        self.cursor = self.connection.cursor()
        # try:
        #     self.cursor.execute("DROP TABLE card;")
        # except:
        #     pass
        try:
            for row in self.cursor.execute("select number, pin, balance from card;"):
                self.accounts[row[0]] = {"pin": int(row[1]), "balance": int(row[2])}
        except sqlite3.OperationalError:
            self.cursor.execute("""CREATE TABLE card(
            id Integer,
            number TEXT,
            pin TEXT,
            balance Integer default 0
            );""")

    def create_account(self):
        while not self.create_card_number():
            pass
        # {card_number:{pin:1234, balance:0}}
        pin = random.randint(1000, 9999)
        self.accounts[self.current_card_number] = {"pin": pin, "balance": 0}
        self.amount_of_users += 1
        self.adding_into_bd(self.current_card_number, pin, 0)
        self.print_massage(1, self.current_card_number)

    def adding_into_bd(self, card_number, pin, balance):
        self.cursor.execute(
            "INSERT INTO card VALUES ({},{},{},{});".format(self.amount_of_users, card_number, pin, balance))
        self.connection.commit()
        # self.cursor.execute("select * from card;")
        # print(self.cursor.fetchone())

    def print_massage(self, option=0, card_number=0):
        if option == 0 and self.state == 0:
            print("1. Create an account\n2. Log into account\n0. Exit")
        elif option == 1 and self.state == 0:
            print("Your card has been created\nYour card number:\n{}\nYour card PIN:\n{}\n".format(card_number,
                                                                                                   self.accounts[
                                                                                                       card_number][
                                                                                                       "pin"]))
        elif self.state == 2:
            print("\nEnter your card number:")
        elif self.state == 21:
            print("Enter your PIN:")
        elif self.state == 22:
            print("\nYou have successfully logged in!\n")
        elif self.state == 3:
            print("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit")

    def log_into_account(self):
        if self.state == 2:
            self.print_massage()
        elif self.state == 21:
            self.print_massage()
        elif self.state == 22:
            if self.current_card_number in self.accounts and self.accounts[self.current_card_number][
                "pin"] == self.current_pin:
                self.print_massage()
                self.state = 3
                self.print_massage()
            else:
                print("\nWrong card number or PIN!\n")
                self.state = 0
                self.print_massage()

    def terminal(self, command):
        if command == "1" and self.state == 0:
            self.create_account()
            self.print_massage()
            return True
        elif command == "2" and self.state == 0:
            self.state = 2
            self.log_into_account()
            return True
        elif self.state == 2:
            self.current_card_number = command
            self.state = 21
            self.log_into_account()
            return True
        elif self.state == 21:
            self.current_pin = int(command)
            self.state = 22
            self.log_into_account()
            return True
        elif self.state == 3:  # Account menu
            if command == "1":
                print("\nBalance: {}\n".format(self.accounts[self.current_card_number]["balance"]))
                self.print_massage()
                return True
            elif command == "2":
                self.state = 32
                print("\nEnter income:")
                return True
            elif command == "3":
                self.state = 33
                print("\nTransfer\nEnter card number:")
                return True
            elif command == "4":
                self.close_account()
                print("\nThe account has been closed!\n")
                self.state = 0
                self.print_massage()
                return True
            elif command == "5":
                print("\nYou have successfully logged out!\n")
                self.state = 0
                self.print_massage()
                return True
            elif command == "0":
                self.ending_program()
                return False
        elif self.state == 32:
            self.update_card_balance(int(command), self.current_card_number)
            print("Income was added!\n")
            self.state = 3
            self.print_massage()
            return True
        elif self.state == 33:
            if self.transfer(command):
                self.state = 34
                self.second_card_number = command
                print("Enter how much money you want to transfer:")
            else:
                self.state = 3
            return True
        elif self.state == 34:
            self.transfer(command)
            self.state = 3
            self.print_massage()
            return True
        elif command == "0":
            self.ending_program()
            return False
        self.ending_program()
        return False

    def close_account(self):
        self.cursor.execute("DELETE FROM card WHERE number = {};".format(self.current_card_number))
        del self.accounts[self.current_card_number]
        self.connection.commit()

    def update_card_balance(self, balance, card_number):
        self.accounts[card_number]["balance"] += balance
        self.cursor.execute(
            "UPDATE card SET balance={} WHERE number = {};".format(self.accounts[card_number]["balance"], card_number))
        self.connection.commit()

    def transfer(self, money_or_card):
        if self.state == 33:
            if money_or_card != self.current_card_number:
                if money_or_card[-1] == self.luhn_algorithm(0, 0, money_or_card[:-1]):
                    if self.check_card_in_db(money_or_card):
                        return True
                    else:
                        print("Such a card does not exist.\n")
                        self.state = 3
                        self.print_massage()
                else:
                    print("Probably you made a mistake in the card number. Please try again!\n")
                    self.state = 3
                    self.print_massage()
            else:
                print("You can't transfer money to the same account!\n")
                self.state = 3
                self.print_massage()
        if self.state == 34:
            if self.accounts[self.current_card_number]["balance"] >= int(money_or_card):
                self.update_card_balance(int(money_or_card), self.second_card_number)
                self.update_card_balance(-int(money_or_card), self.current_card_number)
                print("Success!\n")
            else:
                print("Not enough money!\n")
                self.print_massage()

    def check_card_in_db(self, card):
        self.cursor.execute("SELECT * FROM card WHERE number = {};".format(card))
        return self.cursor.fetchone() is not None

    def ending_program(self):
        print("Bye!")
        self.connection.commit()
        self.connection.close()

    def create_card_number(self):
        account_identifier = random.randint(100_000_000, 999_999_999)
        self.current_card_number = "400000{}{}".format(account_identifier,
                                                       self.luhn_algorithm("400000", account_identifier))
        return not (self.current_card_number in self.accounts)

    def luhn_algorithm(self, bank_identifier_number, account_identifier, card_number=""):
        if card_number == "":
            card_number = list(bank_identifier_number + str(account_identifier))
        else:
            card_number = list(card_number)
        for i in range(0, len(card_number), 2):
            card_number[i] = int(card_number[i]) * 2
            if card_number[i] > 9:
                card_number[i] -= 9
        sum_digits = 0
        for i in range(len(card_number)):
            card_number[i] = int(card_number[i])
            sum_digits += card_number[i]
        return str((10 - sum_digits % 10) % 10)


bank = Bank()
# print(bank.luhn_algorithm(0, 0, "400000894391923"))
# bank.cursor.execute("SELECT * FROM card WHERE number = {};".format("14000009224965429"))
# print(bank.cursor.fetchone())
# print(bank.cursor.rowcount)
# bank.accounts = {1: {"pin": 1, "balance": 0}}
while bank.terminal(input()):
    pass
