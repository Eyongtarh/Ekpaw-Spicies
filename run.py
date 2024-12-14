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
        print("Please enter sales data from the last market.")
        print("Data should be a positive integer.")
        print("Data shall be one at a time\n")


        quantity1 = input("Enter the garlic quantity sold: ").strip()
        quantity2 = input("Enter the leek quantity sold: ").strip()
        quantity3 = input("Enter the onion quantity sold: ").strip()
        quantity4 = input("Enter the okra quantity sold: ").strip()
    
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


def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet updated successfully.\n")

def calculate_profit_loss(sales_row):
    """
    Multiply sales with price to get revenue and multiply sales with cost to get cost.
    calculate the profit_loss for each item type subtracted cost form the revenue:
    -Positive value indicates profiy
    -Negative value indicates loss.
    """
    print("Calculating revenue data...\n")
    revenue = SHEET.worksheet("price").get_all_values()
    price_row = price[-1]

    profit_loss_data = []
    for price, sales in zip(price_row, sales_row):
        revenue = int(price)*sales
        
    print("Calculating cost data...\n")
    cost = SHEET.worksheet("cost").get_all_values()
    cost_row = cost[-1]

    for cost, sales in zip(cost_row, sales_row):
        cost = int(cost)*sales    
    profit_loss_data.append(revenue-cost_data)

    return profit_loss_data

# Main program loop
def main():
    """
    Run all program functions
    """
    while True:
        print("\nWelcome to Ekpaw Spicies Data Automation")

        print("Menu:")
        print("1. Input new data")
        print("2. Display old data")
        print("3. Exit")
        
        choice = input("Enter your choice (1, 2, or 3): \n")
        
        if choice == '1':
            data = get_sales_data()
            sales_data = [int(num) for num in data]
            update_sales_worksheet(sales_data)
            profit_loss_data = calculate_profit_loss(sales_row)
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