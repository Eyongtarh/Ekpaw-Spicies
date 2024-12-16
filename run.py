import numpy as np
from tabulate import tabulate
from simple_term_menu import TerminalMenu
from colorama import just_fix_windows_console
just_fix_windows_console()
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ekpaw_spicies')

def display_data():
    """
    Function to display existing data
    """
    if False:
        print("No data available.")
    else:
        print("Current Data:")
        sales = SHEET.worksheet('sales').get_all_values()
        spicies_revenue = SHEET.worksheet("spicies_revenue").get_all_values()
        spicies_cost = SHEET.worksheet("spicies_cost").get_all_values()
        profit_loss = SHEET.worksheet("profit_loss").get_all_values()
        display_data_to_user()
    print(tabulate(
        'Sales data:',sales,'Revenue data:',spicies_revenue,'Cost data:',
    spicies_cost,'profit/loss data:',profit_loss
    ))

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, one item at a time. The loop will repeatedly request data, 
    until it is valid.
    """
    while True:
        print(f"""
\nPlease enter sales data from the last market.
Data should be a positive whole number.
Data shall be one at a time\n
        """)
        quantity1 = input("Enter the garlic quantity sold:\n").strip()
        quantity2 = input("Enter the leek quantity sold:\n").strip()
        quantity3 = input("Enter the onion quantity sold:\n").strip()
        quantity4 = input("Enter the okra quantity sold:\n").strip()
        data_str = [quantity1, quantity2, quantity3, quantity4]
        sales_data = data_str
        if validate_data(sales_data):
            print("Valid positive integer!")
            break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values] 
        if len(values) != 4:
            raise ValueError (
                f"Exactly 4 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False
    return True

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet... \n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_spicies_revenue(sales_row):
    """
    Multiply sales with selling_pricee to get revenue.
    """
    print("Calculating spicies revenue data...\n")
    selling_prices = SHEET.worksheet("selling_prices").get_all_values()
    selling_prices_row = selling_prices[-1]
    spicies_revenue_data = []
    for selling_prices, sales in zip(selling_prices_row, sales_row):
        revenue = int(selling_prices)*sales
        spicies_revenue_data.append(revenue)
    return spicies_revenue_data

def calculate_spicies_cost(sales_row):
    """
    Multiply sales with cost_prices to get cost of spicies.
    """
    print("Calculating spicies cost data...\n")
    cost_prices = SHEET.worksheet("cost_prices").get_all_values()
    cost_prices_row = cost_prices[-1]

    spicies_cost_data = []
    for cost_prices, sales in zip(cost_prices_row, sales_row):
        cost = int(cost_prices)*sales    
        spicies_cost_data.append(cost)
    return spicies_cost_data

def calculate_profit_loss_data():
    """
    calculate the profit_loss for each item type by subtracting cost form the revenue.
    -Positive value indicates profiy
    -Negative value indicates loss.
    """
    print("Calculating profit_loss data...\n")
    spicies_revenue = SHEET.worksheet("spicies_revenue").get_all_values()
    spicies_revenue_row = spicies_revenue[-1]
    spicies_cost = SHEET.worksheet("spicies_cost").get_all_values()
    spicies_cost_row = spicies_cost[-1]
    profit_loss_data = []
    for spicies_revenue, spicies_cost in zip(spicies_revenue_row, spicies_cost_row):    
        profit_loss = int(spicies_revenue) - int(spicies_cost)
        profit_loss_data.append(profit_loss)
    return profit_loss_data


def display_data_to_user():
    """
    To display current data to user
    Total revenue for last market day sales
    """
    spicies_revenue = SHEET.worksheet("spicies_revenue").get_all_values()
    spicies_revenue_row = spicies_revenue[-1]
    total_spicies_revenue = sum(int(item) for item in spicies_revenue_row)
    print("Total spicies revenue for last market day sales is:")
    print(total_spicies_revenue)
    
    """
    To display current data to user
    Total cost for last market day sales
    """
    spicies_cost = SHEET.worksheet("spicies_cost").get_all_values()
    spicies_cost_row = spicies_cost[-1]
    total_spicies_cost = sum(int(item) for item in spicies_cost_row)
    print("Total spicies cost for last market day sales is:")
    print(total_spicies_cost)

    """
    To display current data to user
    Total profit/loss for last market day sales
    """
    profit_loss = SHEET.worksheet("profit_loss").get_all_values()
    profit_loss_row = profit_loss[-1]
    total_profit_loss = sum(int(item) for item in profit_loss_row)
    print("Total profit for last market day sales is:")
    print(total_profit_loss)
    return total_spicies_revenue, total_spicies_cost, total_profit_loss

def main():
    """
    Run all program functions
    """
    while True:
        print(f"""
\nWelcome to Ekpaw Spicies Data Automation\n
Menu:
1. Input new data
2. Display old data
3. Exit
        """)
        choice = input("Enter your choice (1, 2, or 3): \n")
        
        if choice == '1':
            data = get_sales_data()
            sales_data = [int(num) for num in data]
            update_worksheet(sales_data, "sales")
            new_spicies_revenue = calculate_spicies_revenue(sales_data)
            update_worksheet(new_spicies_revenue, "spicies_revenue")
            new_spicies_cost = calculate_spicies_cost(sales_data)
            update_worksheet(new_spicies_cost, "spicies_cost")
            new_profit_loss = calculate_profit_loss_data()
            update_worksheet(new_profit_loss, "profit_loss")
            display_data_to_user()
            
        elif choice == '2':
            display_data()
        elif choice == '3':
            print("Program exited")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

        """
        Ask if the user wants to add another sales data
        """
        continue_input = input("\nDo you want to enter another sales data? (y/n): ").lower()
        if continue_input != 'y':
            print("Program exited")
            break

if __name__ == "__main__":
    main()