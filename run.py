import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint # pprint is a module that provides a capability to “pretty-print” arbitrary Python data structures in a format that can be used as input to the interpreter.

# Variable to store the scope of the API
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
    
# Variable to store the credentials of the API
CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE) # Uses the with scopes method to pass the scope variable
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS) # Authorizes the client with the credentials
SHEET = GSPREAD_CLIENT.open('love_sandwiches') # Accesses the spreadsheet

# following code is for testing purposes to check if the API is working
# sales = SHEET.worksheet('sales') # Accesses the sales worksheet
# data = sales.get_all_values() # Gets all the values from the worksheet
# print(data) # Prints the data

def get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user via the terminal, which must be a string of 6 numbers separated by commas.
    The loop will repeatedly request data, until it is valid.
    """
    while True: # While loop will run until the user enters the correct data
      print("Please enter sales data from the last market.")
      print("Data should be six numbers, separated by commas.")
      print("Example: 10,20,30,40,50,60\n")

      data_str = input("Enter your data here: ")

      # Takes the data string and splits it into a list of individual strings using the split method, separated by commas
      sales_data = data_str.split(",") # this will remove the commas from the string
      validate_data(sales_data)

      if validate_data(sales_data):
          print("Data is valid!")
          break
    return sales_data

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    # print(values) testing purposes
    try: # Try block will run the code inside it if it is successful
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e: # If the try block fails, the except block will run error message
        print(f"Invalid data: {e}, please try again.\n")
        return False # Returns False if the data is invalid

    return True # Returns True if the data is valid which will break the while loop in the get_sales_data function

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales') # Accesses the sales worksheet declared in the global scope
    sales_worksheet.append_row(data) # Appends the data to the sales worksheet
    print("Sales worksheet updated successfully.\n")

def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock figure.
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values() # Accesses the stock worksheet and gets all the values
    stock_row = stock[-1] # Gets the last row of the stock worksheet, -1 because the index starts at 0
    print(stock_row)


def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] # List comprehension to convert the string values into integers
    update_sales_worksheet(sales_data) # Calls the update_sales_worksheet function with the sales_data list as an argument
    calculate_surplus_data(sales_data) # Calls the calculate_surplus_data function with the sales_data list as an argument

print("Welcome to Love Sandwiches Data Automation")
main() # Calls the main function to run the program 