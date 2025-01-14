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

'''
# This code was refactored into the update_worksheet function

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list data provided.
    """
    print("Updating sales worksheet...\n")
    sales_worksheet = SHEET.worksheet('sales') # Accesses the sales worksheet declared in the global scope
    sales_worksheet.append_row(data) # Appends the data to the sales worksheet
    print("Sales worksheet updated successfully.\n")

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating surplus worksheet...\n")
    surplus_worksheet = SHEET.worksheet('surplus') # Accesses the surplus worksheet declared in the global scope
    surplus_worksheet.append_row(data) # Appends the data to the surplus worksheet
    print("Surplus worksheet updated successfully.\n")
'''

def update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Updates the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet) # Accesses the worksheet passed as an argument
    worksheet_to_update.append_row(data) # Appends the data to the worksheet
    print(f"{worksheet} worksheet updated successfully.\n")
    

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
    
    surplus_data = [] # Empty list to store the surplus data
    for stock, sales in zip(stock_row, sales_row): # Uses the zip function to iterate over both lists at the same time
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the last 5 entries for each sandwich and returns the data as a list of lists.
    """
    sales = SHEET.worksheet("sales") # Accesses the sales worksheet

    columns = [] # Empty list to store the columns
    for ind in range(1, 7): # For loop to iterate over the range of 1 to 7 as there are 6 columns
        column = sales.col_values(ind)
        # Appends the last 5 values of each column to the columns list
        columns.append(column[-5:]) # uses the slice method to get the last 5 values of each column, the colon is used to slice the list
    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = [] # Empty list to store the new stock data

    for column in data: # For loop to iterate over the data list
        int_column = [int(num) for num in column] # List comprehension to convert the string values into integers
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

def main():
    """
    Run all program functions.
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data] # List comprehension to convert the string values into integers
    update_worksheet(sales_data, "sales") # Calls the update_worksheet function with the sales_data list and the sales worksheet as arguments
    new_surplus_data = calculate_surplus_data(sales_data) # Calls the calculate_surplus_data function with the sales_data list as an argument
    update_worksheet(new_surplus_data, "surplus") # Calls the update_worksheet function with the new_surplus_data list and the surplus worksheet as arguments
    sales_columns = get_last_5_entries_sales() # Calls the get_last_5_entries_sales function
    stock_data = calculate_stock_data(sales_columns) # Calls the calculate_stock_data function with the sales_columns list as an argument
    update_worksheet(stock_data, "stock") # Calls the update_worksheet function with the stock_data list and the stock worksheet as arguments
    
    print(stock_data) # Prints the stock data to the terminal

print("Welcome to Love Sandwiches Data Automation")
main() # Calls the main function to run the program 
