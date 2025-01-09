import gspread
from google.oauth2.service_account import Credentials

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
    Get sales figures input from the user
    """
    print("Please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60")

    data_str = input("Enter your data here: ")
    print(f"The data provided is {data_str}")
    
print("Script is running")
get_sales_data()