import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figures input from the user. While loop will keep
    asking for input until valid values are provided. Validate_data
    function called to check on the inputs provided.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
       
        sales_data = data_str.split(",")
        if validate_data(sales_data):
            print("Data is valid!")
            break
    return sales_data


def validate_data(values):
    """
    Inside the try converts all string values to integers.
    Raises ValueError if strings cannot be converted or there aren't 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data {e}, please try again.\n")
        return False
    
    return True


def calculate_surplus_data(sales_row):
    """
    Compare sales data with stock and calculate the surplus
    for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive suplus indicates waste.
    - Negative surplus indicates extra made to order after stock.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    stock_data = [int(num) for num in stock_row]

    surplus_data = []
    for stock, sales in zip(stock_data, sales_row):
        surplus = stock - sales
        surplus_data.append(surplus)
    return surplus_data


def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into worksheet
    updates relevant worksheet with this data.
    """
    print(f"updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully.\n")


def previous_sales():
    """
    Collects columns of data from sales worksheets, collects
    previous 5 days of sales for these, and then returns the average for
    those 5 days plus 10% rounded to nearest whole number.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    pprint(columns)


def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")


# print("Welcome to Love Sandwiches")
# main()

previous_sales()