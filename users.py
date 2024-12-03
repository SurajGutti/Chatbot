from tinydb import TinyDB, Query
import re

db = TinyDB("user_data.json")
query = Query()


# registering a new user
def create_user():
    try:
        # Till user selects a valid user name
        while True:
            name = input("Choose a new username (letters only) or type 'cancel' to exit: ")
            if name.lower() == "cancel":
                print("Iris: You have exited the registration process.")
                return None

            # Check if user name has no numbers or special characters
            if not re.match("^[A-Za-z]+$", name):
                print("Iris: Invalid username. User name cannot contain numbers or special characters.")
                continue
            # if user with the name already exists
            if db.search(query.name == name):
                print(f'Iris: Username {name} already exists. Please choose a different username.')
                continue
            break

        # assign password. Can be anything
        password = input("Enter a new password or type 'cancel' to exit: ")
        if password.lower() == "cancel":
            print("Iris: You have exited the registration process.")
            return

        # Create user in database
        db.insert({'name': name, 'password': password})
        print("Iris: Registration successful! You can now log in with your new account.")
        return
    except Exception as e:
        print(f'Iris: An error occurred: {e}')


# Check if user exists. Also used to logging in
def authenticate(name, password):
    try:
        user = db.search((query.name == str(name)) & (query.password == str(password)))
        if user:
            return True
        else:
            print(f'Iris: Authentication failed. Please check your username or password. If you are a new user, '
                  f'please register an account by typing "register"')
            return False
    except Exception as e:
        print(f'An error occurred: {e}')


# Permanently deletes a user account
def delete_user(name):
    try:
        # Confirm deletion with password
        password = input("Enter your password to confirm or type 'cancel': ")
        if password.lower() == "cancel":
            print("Iris: Account deletion canceled.")
            return

        # Authenticate the user
        authentication = authenticate(name, password)
        if authentication is False:
            print("Iris: Authentication failed. Please check your password.")
            return

        # Remove user
        db.remove(query.name == str(name))
        print(f"Iris: I'm sorry to see you go {name}. Your account has been deleted successfully.")
        return
    except Exception as e:
        print(f'An error occurred: {e}')
