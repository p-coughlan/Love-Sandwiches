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
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")

    # Takes the data string and splits it into a list of individual strings using the split method, separated by commas
    sales_data = data_str.split(",") # this will remove the commas from the string
    validate_data(sales_data)

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try: # Try block will run the code inside it if it is successful
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e: # If the try block fails, the except block will run error message
        print(f"Invalid data: {e}, please try again.\n")

    
get_sales_data()

 