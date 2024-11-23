import scratchattach as scratch3
import json
import os

# Replace with your actual session_id, username, and project_id
SESSION_ID = "SESSION-ID"
USERNAME = "USERNAME"
PROJECT_ID = "PROJECT-ID"

# JSON file to store account information
ACCOUNTS_FILE = "accounts.json"

# Function to load accounts from the JSON file
def load_accounts():
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    else:
        return {}

# Function to save accounts to the JSON file
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

# Function to add a new account
def add_account(username, password, scratch_username):
    accounts = load_accounts()
    if username not in accounts:
        accounts[username] = {
            "password": password,
            "scratch_username": scratch_username
        }
        save_accounts(accounts)
        print(f"Account created for {username}.")
    else:
        print(f"Account for {username} already exists.")

# Function to authenticate an account
def authenticate_account(username, password):
    accounts = load_accounts()
    if username in accounts and accounts[username]["password"] == password:
        print(f"User {username} authenticated successfully.")
        return True
    else:
        print(f"Authentication failed for {username}.")
        return False

# Function to check if a Scratch username exists
def check_scratch_username(scratch_username):
    accounts = load_accounts()
    for account in accounts.values():
        if account.get("scratch_username") == scratch_username:
            return True
    return False

# Set up the Scratch session and connection
session = scratch3.Session(SESSION_ID, username=USERNAME)
try:
    conn = session.connect_cloud(PROJECT_ID)
    print("Connected to Scratch project.")
except Exception as e:
    print(f"Failed to connect to Scratch project: {e}")

client = scratch3.CloudRequests(conn)

@client.request
def login(combined_username, password):
    print("Login request received.")
    try:
        username, scratch_username = combined_username.split("/")
    except ValueError:
        return "Invalid format for username. Use 'username/scratch_username'."
    
    print(f"Received login request with username: {username}, password: {password}, and scratch_username: {scratch_username}")

    if authenticate_account(username, password):
        return f"Welcome back, {username}!"
    else:
        return f"Account: {username}, does not exist."

@client.request
def check_user(scratch_username):
    print(f"Check user request received for Scratch username: {scratch_username}")
    if check_scratch_username(scratch_username):
        return f"Scratch username {scratch_username} exists."
    else:
        return f"Scratch username {scratch_username} does not exist."

@client.request
def create_account(username, password, scratch_username):
    print(f"Create account request received for username: {username}, Scratch username: {scratch_username}")
    accounts = load_accounts()
    if username in accounts:
        return f"Account for username {username} already exists."
    if check_scratch_username(scratch_username):
        return f"Scratch username {scratch_username} is already associated with another account."
    add_account(username, password, scratch_username)
    return f"Account created successfully for {username}."

@client.event
def on_ready():
    print("Request handler is running")

# Run the client with error handling
try:
    client.run()
except Exception as e:
    print(f"Error running client: {e}")
