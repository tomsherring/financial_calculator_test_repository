import math

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

        print(
            f"\nBased on an initial investment of £{
                deposit_f}, with an interest rate of "
            f"{int_rate_f}% over {num_years_f} years, you will receive £{a_f}"
        )

    return wrapper


# Decorator to wrap the return values from bond_calulator() in text.
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


# Investment calulator. Returns 1 of 2 equations based on user input.
# Ideally I would apply defensive programming here to ensure the user input is valid;
# however, this is outside of the scope of the brief.
@investment_calc_decorator
def investment_calulator():
    print("\nThank you for selecting the investment calculator\n")
    deposit = float(
        input("Please enter the total amount you wish to invest: "))
    interest_rate = float(input("Please enter the interest rate: "))
    num_years = float(input("How many years do you plan to invest: "))
    simple_or_compound = input(
        "Please indicate if you want a 'simple' or 'compound' investment instrument?: "
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
    print("\nThank you for selecting the bond interest repayment calculator\n")
    house_value = float(input("What is the current value of your house: "))
    interest = float(input("Please enter the interest rate: "))
    num_months = float(
        input(
            "Please enter the number of months over which you intnd to repay the loan: "
        )
    )
    i = (interest / 100) / 12

    # repayment = (i * P)/(1 - (1 + i)**(-n))
    repayment = (i * house_value) / (1 - (1 + i) ** -num_months)

    return house_value, interest, num_months, round(repayment, 2)


# The below selector func executes at the beginning of the program.
# It prompts the user to choose between the two calcualtor funcs.
# If the user doesn't make a correct selection/input, they are prompted to try again.


# I am using a while loop here to keep the program running until the user exits.
def calculator_selector():
    while True:
        calculator_selection = input(
                "\nThank you for choosing CoGrammer's financial calculators. Please choose either: \n\n"
                "investment - to calculate the amount of interest you'll earn on your investment \n"
                "bond       - to calculate the amount you'll have to pay on a home loan \n\n"
                "Enter either 'investment' or 'bond' from the menu above to proceed: "
            )
        
        if calculator_selection.lower().strip() == "investment":
            investment_calulator()
        elif calculator_selection.lower().strip() == "bond":
            bond_calculator()
        else:
            print("\nThis is not a valid input. Please try again.")


def main():
    calculator_selector()


if __name__ == "__main__":
    main()
