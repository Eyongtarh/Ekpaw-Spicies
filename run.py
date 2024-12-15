import numpy as np
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

# Function to display existing data
def display_data():
    if False:
        print("No data available.")
    else:
        print("Current Data:")
        sales = SHEET.worksheet('sales')
        data = sales.get_all_values()
    print(data)

# Function to input new data
def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, one item at a time. The loop will repeatedly request data, 
    until it is valid.
    """
    while True:
        print("\nPlease enter sales data from the last market.")
        print("Data should be a positive integer.")
        print("Data shall be one at a time\n")


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
    Multiply sales with cost_prices to get cost.
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
    calculate the profit_loss for each item type by subtracting cost form the revenue:
    -Positive value indicates profiy
    -Negative value indicates loss.
    """

    print("Calculating profit_loss data...\n")
    spicies_revenue = SHEET.worksheet("spicies_revenue").get_all_values()
    spicies_revenue_row = spicies_revenue[-1]
    
    profit_loss_data = []
    for spicies_revenue, spicies_cost in zip(spicies_revenue, spicies_cost):
        profit_loss = [a - b for a, b in zip(spicies_revenue - spicies_cost)]
        profit_loss_data.append(profit_loss)

    return profit_loss_data

# Main program loop
def main():
    """
    Run all program functions
    """
    while True:
        print("\nWelcome to Ekpaw Spicies Data Automation\n")

        print("Menu:")
        print("1. Input new data")
        print("2. Display old data")
        print("3. Exit")
        
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
            
        elif choice == '2':
            display_data()
        elif choice == '3':
            print("Exiting the program...")
            break
        else:
            print("Invalid choice. Please choose 1, 2, or 3.")

        # Ask if the user wants to add another transaction
        continue_input = input("\nDo you want to enter another transaction? (y/n): ").lower()
        if continue_input != 'y':
            break



if __name__ == "__main__":
    main()