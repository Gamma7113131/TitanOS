import json
import os

# JSON file to store account information
ACCOUNTS_FILE = "accounts.json"

def load_accounts():
    """Load accounts from the JSON file."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_accounts(accounts):
    """Save accounts to the JSON file."""
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

def add_account(username, password):
    """Add a new account."""
    accounts = load_accounts()
    if username not in accounts:
        accounts[username] = {
            "password": password,
        }
        save_accounts(accounts)
        return f"Account created for {username}."
    return f"Account for {username} already exists."

def authenticate_account(username, password):
    """Authenticate an account."""
    accounts = load_accounts()
    if username in accounts and accounts[username]["password"] == password:
        return True, f"User {username} authenticated successfully."
    return False, f"Authentication failed for {username}."


def create_account(username, password):
    """Create a new account."""
    accounts = load_accounts()
    if username in accounts:
        return f"Account for username {username} already exists."
    return add_account(username, password)

def check_username(username):
    accounts = load_accounts()
    if username in accounts:
        return True
    return False

# API for main.py to use
def process_login(username, password):
    """Process a login request."""   
    success, message = authenticate_account(username, password)
    return success

def process_check_user(username):
    """Check if a Scratch username exists."""
    return check_username(username)

def process_create_account(username, password):
    """Process account creation."""
    return create_account(username, password)


def update_data(name, username, data):
    accounts = load_accounts()
    if username in accounts:
        accounts[username][name] = data
        save_accounts(accounts)
        return True
    else:
        return False

def get_data(name, username):
    accounts = load_accounts()
    if username in accounts and name in accounts[username]:
        return accounts[username][name]
    return False
