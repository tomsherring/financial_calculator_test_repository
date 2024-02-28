import math
import requests
import datetime

api_url = 'https://api.api-ninjas.com/v1/interestrate'
headers = {'X-Api-Key': 'U45SfaZ3E304c67incPLNQ==KRN7igB5BKGAaEsC'}
params = {
    'country': 'United Kingdom',
}
response = requests.get(api_url, headers=headers, params=params)
if response.status_code == 200:
    data = response.json()

    # Use a for loop to iterate through the list of dictionaries
    for rate_info in data['central_bank_rates']:
        if rate_info['country'] == 'United Kingdom':
            uk_interest_rate = rate_info['rate_pct']
            last_updated = rate_info['last_updated']
            #print("UK Interest Rate:", uk_interest_rate)
            #print("Last Updated:", last_updated)
            break  # Exit the loop after finding the UK data
else:
    print("Error:", response.status_code)


date_object = datetime.datetime.strptime(last_updated, '%m-%d-%Y')

formatted_date = date_object.strftime('%d/%m/%Y')


# Brief: You have been approached by a financial services company to
# create a program that allows the user to choose between two calculators.
# 1.An investment calculator.
# 2. a bond repayment calculator.
# Design a Python program to deliver this functionality.
# - Aim for modularity for maximum code reusability.

# Part 1:
# The program should prompt the user to choose an investment calculator.
# NB. The input should be case insensitive. Use .lower().strip() to clean inputs.

# investment - to calculate the amount of interest you'll earn on your investment
# bond       - to calculate the amount you'll have to pay on a home loan
# Enter either 'investment' or 'bond' from the menu above to proceed:

# Part 2:
# if choosing the 'investment calculator'
# ask the user to input the amount of money they are depositing
# ask the user to input the interest rate as a numerical value
# ask the user for the number of years they plan on investing
# ask the user if they want simple or compound interest.
# Store this in a value call interest.
# using the variables above, calculate how much interest will be returned to the customer.
# Simple interest equation:  A = P *(1 + r*t)
# Compound interest equation: A = P * math.pow((1+r),t)
# use a decorator to wrap output text

# Part 3:
# If choosing bond calculator:
# ask the user to input the current value of their house.
# ask the user to input the current interest rate
# The number of months they plan to take to repay the bond
# Interest repayment calculation: repayment = (i * P)/(1 - (1 + i)**(-n))
# use a decorator to wrap output text


# Decorator to wrap the return values from investment_calutor() in text.
def investment_calc_decorator(func):
    def wrapper(*args, **kwargs):
        deposit, interest_rate, num_years, a = func(*args, **kwargs)

        # eval if the *args (floats) can be passed as ints. Extra code but, I want to
        # format as an ints if poss as floats look ugly here (5.0 years i.e.)
        deposit_f = int(deposit) if deposit.is_integer() else deposit
        int_rate_f = int(
            interest_rate) if interest_rate.is_integer() else interest_rate
        num_years_f = int(num_years) if num_years.is_integer() else num_years
        a_f = int(a) if a.is_integer() else a

        print(f"Based on an initial investment of £{deposit_f}", end=" ")
        print(f"with an interest rate of {int_rate_f}% over", end=" ")
        print(f"{num_years_f} years, you will receive £{a_f}", end=" ")
        print("at the end of the term.")

    return wrapper


# Decorator to wrap the return values from bond_calculator() in text.
def bond_calc_decorator(func):
    def wrapper(*args, **kwargs):
        house_value, interest, num_months, repayment = func(*args, **kwargs)

        house_val_f = int(
            house_value) if house_value.is_integer() else house_value
        interest_f = int(interest) if interest.is_integer() else interest
        num_months_f = int(
            num_months) if num_months.is_integer() else num_months
        repayment_f = int(repayment) if repayment.is_integer() else repayment

        print(
            f"\nBased on the loan amount of £{house_val_f} at a {interest_f}% "
            f"rate of interest, you would need to make {num_months_f} monthly"
            f"repayments of £{repayment_f}"
        )

    return wrapper


# Investment calculator. Returns 1 of 2 equations based on user input.
# Ideally I would apply defensive programming here to ensure the user input is valid;
# however, this is outside of the scope of the brief.
@investment_calc_decorator
def investment_calculator():
    print("\nThank you for selecting the investment calculator\n")
    deposit = float(
        input("Please enter the total amount you wish to invest: "))
    interest_rate = float(uk_interest_rate)
    num_years = float(input("How many years do you plan to invest: "))
    simple_or_compound = input(
        "Please choose a 'simple' or 'compound' savings account?: "
    )
    # how to return this as yes/no or true/false
    r = interest_rate / 100

    if simple_or_compound.lower().strip() == "simple":
        # A = P *(1 + r*t)
        a = deposit * (1 + (r * num_years))

        return deposit, interest_rate, num_years, round(a, 2)

    elif simple_or_compound.lower().strip() == "compound":
        # A = P * math.pow((1+r),t)
        a = deposit * math.pow((1 + r), num_years)

        return deposit, interest_rate, num_years, round(a, 2)


# Bond calculator. Returns the bond repayment amount based on user input.
@bond_calc_decorator
def bond_calculator():
    print("")
    print("Thank you for selecting the bond interest repayment calculator.")
    print("")
    house_value = float(input("What is the current value of your house: "))
    interest = float(uk_interest_rate)
    num_months = float(
        input(
            "Please enter the length of the loan (months): "
        )
    )
    i = (interest / 100) / 12

    # repayment = (i * P)/(1 - (1 + i)**(-n))
    repayment = (i * house_value) / (1 - (1 + i) ** -num_months)

    return house_value, interest, num_months, round(repayment, 2)


# The below selector func executes at the beginning of the program.
# It prompts the user to choose between the two calculator functions.
# If the user doesn't make a correct selection/input, they are prompted to try again.


# I am using a while loop here to keep the program running until the user exits.
def calculator_selector():

    print(f"""
              
    Thank you for choosing CoGrammer's financial calculators. 
    This program will help you calculate the amount of interest you'll earn on
    an investment, or the amount you'll have to pay on a home loan.
    
    The interest rate available is tied to the UK central bank rate, currently
    set at {uk_interest_rate}%, updated {formatted_date}.
        
    Please choose either:
    investment - to calculate the amount of interest you'll earn on your investment
    bond       - to calculate the amount you'll have to pay on a home loan
    """)

    while True:
        calculator_selection = input(
            "Please enter 'investment' or 'bond' from the menu above to proceed: "
        )

        if calculator_selection.lower().strip() == "investment":
            investment_calculator()
        elif calculator_selection.lower().strip() == "bond":
            bond_calculator()
        else:
            print("\nThis is not a valid input. Please try again.")


def main():
    calculator_selector()


if __name__ == "__main__":
    main()