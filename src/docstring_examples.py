class BankAccount:
    """
    This class represents a bank account with various functionalities.

    Attributes:
        account_holder (str): The name of the account holder.
        balance (float): The current balance of the account.

    Methods:
        __init__(account_holder, balance=0):
            Initialize a BankAccount instance.
        deposit(amount):
            Deposit funds into the account.
        withdraw(amount):
            Withdraw funds from the account.
        get_balance():
            Get the current balance of the account.
        __str__():
            Return a formatted string representation of the account.
    """
    
    def __init__(self, account_holder, balance=0):
        """
        Initialize a BankAccount instance with an account holder and an optional initial balance.
        
        Parameters:
        account_holder (str): The name of the account holder.
        balance (float, optional): The initial balance. Default is 0.
        """
        self.account_holder = account_holder
        self.balance = balance
        
    # Rest of the class code...

def add_numbers(a, b):
    """
    Adds two numbers and returns the result.
    
    Parameters:
    a (int): The first number.
    b (int): The second number.
    
    Returns:
    int: The sum of a and b.
    """
    return a + b