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

def add_account(username, password, scratch_username):
    """Add a new account."""
    accounts = load_accounts()
    if username not in accounts:
        accounts[username] = {
            "password": password,
            "scratch_username": scratch_username
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

def check_scratch_username(scratch_username):
    """Check if a Scratch username exists in the accounts."""
    accounts = load_accounts()
    for account in accounts.values():
        if account.get("scratch_username") == scratch_username:
            return True
    return False

def create_account(username, password, scratch_username):
    """Create a new account."""
    accounts = load_accounts()
    if username in accounts:
        return f"Account for username {username} already exists."
    if check_scratch_username(scratch_username):
        return f"Scratch username {scratch_username} is already associated with another account."
    return add_account(username, password, scratch_username)

# API for main.py to use
def process_login(combined_username, password):
    """Process a login request."""
    try:
        username, scratch_username = combined_username.split("/")
    except ValueError:
        return "Invalid format for username. Use 'username/scratch_username'."
    
    success, message = authenticate_account(username, password)
    return message

def process_check_user(scratch_username):
    """Check if a Scratch username exists."""
    if check_scratch_username(scratch_username):
        return f"Scratch username {scratch_username} exists."
    return f"Scratch username {scratch_username} does not exist."

def process_create_account(username, password, scratch_username):
    """Process account creation."""
    return create_account(username, password, scratch_username)
