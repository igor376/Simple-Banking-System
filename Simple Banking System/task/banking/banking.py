import random


class Bank:
    def __init__(self):
        # 0 - main menu, 2 - Log into account
        self.state = 0
        self.accounts = {}
        self.print_massage()
        self.current_card_number = 0
        self.current_pin = 0

    def create_account(self):
        while not self.create_card_number():
            pass
        # {card_number:{pin:1234, balance:0}}
        self.accounts[self.current_card_number] = {"pin": random.randint(1000, 9999), "balance": 0}
        self.print_massage(1, self.current_card_number)

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
            print("1. Balance\n2. Log out\n0. Exit")

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
        elif self.state == 3:
            if command == "1":
                print("\nBalance: {}\n".format(self.accounts[self.current_card_number]["balance"]))
                self.print_massage()
                return True
            elif command == "2":
                print("\nYou have successfully logged out!\n")
                self.state = 0
                self.print_massage()
                return True
            elif command == "0":
                print("Bye!")
                return False
        elif command == "0":
            print("Bye!")
            return False

    def create_card_number(self):
        account_identifier = random.randint(100_000_000, 999_999_999)
        self.current_card_number = "400000{}{}".format(account_identifier,
                                                       self.luhn_algorithm("400000", account_identifier))
        return not (self.current_card_number in self.accounts)

    def luhn_algorithm(self, bank_identifier_number, account_identifier):
        card_number = list(bank_identifier_number + str(account_identifier))
        for i in range(0, len(card_number), 2):
            card_number[i] = int(card_number[i]) * 2
            if card_number[i] > 9:
                card_number[i] -= 9
        sum_digits = 0
        for i in range(len(card_number)):
            card_number[i] = int(card_number[i])
            sum_digits += card_number[i]
        return str(10 - sum_digits % 10)


bank = Bank()
# bank.accounts = {1: {"pin": 1, "balance": 0}}
while bank.terminal(input()):
    pass
