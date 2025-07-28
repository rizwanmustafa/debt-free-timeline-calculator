# This script has been inspired by Mr Dave Ramsey


from typing import List


# TODO: Implement validation from user input

# For now we assume that debt payments are monthly, I am not a real finance guy
# We also assume that minimum payments are fixed
# We will also assume the snowball method is the preferred method
class Debt:
    def __init__(self, name: str, balance: float, interest_rate: float, min_payment: float):
        self.name = name
        self.balance = balance
        self.interest_rate = interest_rate
        self.min_payment = min_payment
    
    def get_next_month_debt(self):
        return Debt(self.name, self.balance + self.balance * self.interest_rate, self.interest_rate, self.min_payment)
    
    def make_payment(self, payment: float):
        self.balance -= payment
    
    def __str__(self) -> str:
        return f"Name: {self.name}\nBalance: {self.balance}\nInterest Rate: {self.interest_rate * 100}%\nMin Payment: {self.min_payment}"

def get_user_debts() -> List[Debt]:
    debts_complete = False
    debts  : List[Debt]= []

    debt_num = 1
    while not debts_complete:
        name = input(f"Enter debt {debt_num} name: ")
        balance = float(input(f"Enter debt {debt_num} balance (Example: 1700): "))
        interest_rate = float(input(f"Enter debt {debt_num} interest rate (Example: 8): "))
        min_payment = float(input(f"Enter debt {debt_num} min payment (Example: 300): "))

        interest_rate /= 100

        debts.append(Debt(name, balance, interest_rate, min_payment))
        debt_num += 1

        
        user_choice = input("Would you like to continue [Y/n]: ")
        if user_choice.strip().lower() == 'n': debts_complete = True

    return debts

def get_total_debt_amount(debts: List[Debt]) -> float:
    total_balance = 0.0
    for debt in debts:
        total_balance += debt.balance
    
    return total_balance

def get_debt_free_timeline(debts: List[Debt], monthly_income: float):

    remaining_debt = get_total_debt_amount(debts)

    month_number = 1
    
    while remaining_debt > 0:
        remaining_income = monthly_income
        smallest_debt_index = -1
        smallest_debt_balance = -1

        for index, debt in enumerate(debts):
            if debt.balance <= 0: continue

            debt.make_payment(debt.min_payment)
            remaining_income -= min(debt.balance, debt.min_payment)
            print(f'Month {month_number}: You pay {debt.min_payment} to {debt.name}')

            if debt.balance == 0:
                print(f'Month {month_number}: Congratulations, you paid off the {debt.name} debt completely!')
                continue

            
            if smallest_debt_index == -1 or smallest_debt_balance > debt.balance:
                smallest_debt_index = index

        if remaining_income < 0: 
            raise Exception('Income not enough!')
        
        if remaining_income == 0: continue

        if smallest_debt_index == -1:
            raise Exception('Could not find the smallest debt when it was possible!')

        debts[smallest_debt_index].make_payment(remaining_income)
        print(f'Month {month_number}: You pay {remaining_income} to {debts[smallest_debt_index].name}')

        

        
        remaining_income = monthly_income
        month_number += 1
        remaining_debt = get_total_debt_amount(debts)

    print(f'Congratulations, you will be completely debt free on Month {month_number}')

    
if __name__ == "__main__":
    debts = get_user_debts()
    monthly_income = float(input("Enter the amount of money you can spare for debt payments monthly (Example: 1700): "))
    get_debt_free_timeline(debts, monthly_income)