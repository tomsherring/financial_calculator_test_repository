"""
This script is a financial calculator that allows users to calculate
the amount of interest they'll earn on an investment or the amount
they'll have to pay on a home loan.

It makes use of the requests library to make an API call to retrieve
the current interest rate from the API-Ninjas interest rate endpoint.

The user can choose between the investment calculator and the bond
calculator. 

The investment calculator calculates the investment amount based on
user inputs such as the initial deposit, duration of investment,
and type of savings account (simple or compound).

The bond calculator calculates the bond repayment amount based on user
inputs such as the current value of the house, and length of the loan
in months.

The interest rate used in both calculators is tied to the UK central
bank rate, which is retrieved from the API call.
"""

# Import relevant libraries
import math
import requests
import datetime

def call_interest_rate_api():
    # Use the requests library to make an API call
    # Linked to to the API-Ninjas interest rate endpoint
    api_url = 'https://api.api-ninjas.com/v1/interestrate'
    headers = {'X-Api-Key': 'U45SfaZ3E304c67incPLNQ==KRN7igB5BKGAaEsC'}
    params = {
        'country': 'United Kingdom',
    }
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()

        # Select the UK interest rate and last updated date
        for rate_info in data['central_bank_rates']:
            if rate_info['country'] == 'United Kingdom':
                uk_interest_rate = rate_info['rate_pct']
                last_updated = rate_info['last_updated']
                break  # Exit the loop after finding the UK data
    else:
        print("Error:", response.status_code)

    # Format the date to UK standard
    date_object = datetime.datetime.strptime(last_updated, '%m-%d-%Y')
    formatted_date = date_object.strftime('%d/%m/%Y')

    return uk_interest_rate, formatted_date

def investment_calc_decorator(func):
    def wrapper(*args, **kwargs):
        """
        This is a wrapper function that formats the input arguments
        and prints the result.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        deposit, interest_rate, num_years, a = func(*args, **kwargs)

        # Format the return values to integers if they are whole numbers
        deposit_f = int(deposit) if deposit.is_integer() else deposit
        int_rate_f = int(
            interest_rate) if interest_rate.is_integer() else interest_rate
        num_years_f = (
            int(num_years) if num_years.is_integer() else num_years
        )
        a_f = int(a) if a.is_integer() else a

        print(f"Based on an initial investment of £{deposit_f}", end=" ")
        print(f"with an interest rate of {int_rate_f}% over", end=" ")
        print(f"{num_years_f} years, you will receive £{a_f}", end=" ")
        print("at the end of the term.")

    return wrapper


# Decorator to wrap the return values from bond_calculator() in text
def bond_calc_decorator(func):
    def wrapper(*args, **kwargs):
        """
        A decorator function that formats and prints the loan details.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        house_value, interest, num_months, repayment = func(*args, **kwargs)

        house_val_f = int(
            house_value) if house_value.is_integer() else house_value
        interest_f = int(interest) if interest.is_integer() else interest
        num_months_f = int(
            num_months) if num_months.is_integer() else num_months
        repayment_f = int(repayment) if repayment.is_integer() else repayment

        print("")
        print(f"Based on the loan amount of £{house_val_f} at", end=" ")
        print(f" a {interest_f}% rate of interest, you would", end=" ")
        print(f"make {num_months_f} monthly repayments of £{repayment_f}")

    return wrapper


@investment_calc_decorator
def investment_calculator():
    """
    Calculates the investment amount based on user inputs.

    Returns:
    a tuple containing:
        - Deposit (float): the initial deposit amount 
        - Interest rate(float): Current ROI
        - Total years (float): The duration of the investment
        - A (float): The total amount after the investment period
    """

    print("\nThank you for selecting the investment calculator\n")
    deposit = float(
        input("Please enter the total amount you wish to invest: "))
    interest_rate = float(call_interest_rate_api()[0])
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
    """
    Calculates the monthly repayment amount for a bond based on the
    current value of the house, the interest rate, and the loan
    repayment length.

    Returns
    a tuple containing:
        - house_value (float): The current value of the house.
        - interest (float): The interest rate.
        - num_months (float): The loan repayment length in months.
        - repayment (float): The monthly repayment amount.
    """

    print("")
    print("Thank you for selecting the bond interest", end=" ")
    print("calculator. Please enter the following details:")
    print("")
    house_value = float(input("What is the current value of your house: "))
    interest = float(call_interest_rate_api()[0])
    num_months = float(
        input(
            "Please select loan repayment length (months): "
        )
    )
    i = (interest / 100) / 12

    # repayment = (i * P)/(1 - (1 + i)**(-n))
    repayment = (i * house_value) / (1 - (1 + i) ** -num_months)

    return house_value, interest, num_months, round(repayment, 2)


def calculator_selector():
    """
    Displays a welcome message and prompts the user to choose between
    investment and bond calculators.

    If the user selects 'investment', it calls the 
    investment_calculator function.

    If the user selects 'bond', it calls the bond_calculator function.
    """
    # welcome message and main menu
    print(f"""
    
    Welcome to the Financial Services Calculator. 
    This program will help you calculate the amount of interest you'll
    earn on an investment, or the amount you'll have to pay on a home
    loan.
    
    The interest rate for loans and bonds is tied to the UK central
    bank rate, currently set at {call_interest_rate_api()[0]}%, updated 
    {call_interest_rate_api()[1]}.
        
    Please choose either:
    Investment 
    - calculate the amount of interest you'll earn on your investment
    
    or

    Bond       
    - calculate the amount you'll have to pay on a home loan
    """
          )

    # Prompt the user to select a calculator
    calculator_selection = input(
        "Please enter 'investment' or 'bond' from the menu above to proceed: "
    )
    # Call the relevant calculator function based on user input
    if calculator_selection.lower().strip() == "investment":
        investment_calculator()
    elif calculator_selection.lower().strip() == "bond":
        bond_calculator()
    else:
        print("")
        print("This is not a valid input. Please try again.")


def main():
    calculator_selector()


if __name__ == "__main__":
    main()
