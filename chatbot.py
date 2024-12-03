import random

from processor import initialize, intent_match
from applications import new_application, get_status, withdraw_application  # Helper methods regarding applications
from users import create_user, authenticate, delete_user                    # Helper methods regarding users

# context tracking variable
current_context = None
# set up patterns list, patterns dataframe, tags and the entire data from the intents file
pattern_list, patterns_df, pattern_tags, data = initialize()


# Primary chat function
def chat():
    user_name = None  # To track the username to perform tasks (like add to, remove from database)
    confidence_threshold = 0.7  # Set a confidence threshold. For confidence below this value, an error message is shown
    global current_context  # Global variable to track context across user inputs

    print("Iris: Hello! I am Iris. What can I help you with today? (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            print("See you next time!")
            break

        # Get the appropriate tag
        tag = intent_match(inp, pattern_list, patterns_df, pattern_tags, confidence_threshold)

        for tg in data["intents"]:
            if tg['tag'] == tag:
                # if - else statements to deal with special cases like task completions
                # If user types confirms
                if tag == "confirmation":
                    # if there is no context, it means the user just said confirm to nothing
                    if not current_context:
                        tag = "error"
                    # For all other available contexts, perform the appropriate task
                    # Create new application for prepaid card
                    elif current_context == "prepaid":
                        new_application(user_name, "pre-paid")
                        current_context = None
                        break
                    # New application for post paid card
                    elif current_context == "postpaid":
                        new_application(user_name, "post-paid")
                        current_context = None
                        break
                    # Withdraw active application
                    elif current_context == "withdraw":
                        withdraw_application(user_name)
                        current_context = None
                        break
                    # Logout
                    elif current_context == "logout":
                        user_name = None
                        print("Iris: You logged out successfully!")
                        current_context = None
                        break
                    # Delete user
                    elif current_context == "delete_account":
                        delete_user(user_name)
                        user_name = None
                        current_context = None
                        break

                # Upon declination
                elif tag == "decline":
                    if not current_context:
                        tag = "error"
                    else:
                        print("Iris: Action cancelled by user.")
                        current_context = None
                        break

                # New user registration
                elif tag == "register":
                    user_name = create_user()
                    break

                # If user asks their name
                elif tag == "name":
                    if not user_name:
                        print("Iris: You are not currently logged in!")
                        break
                    tg['responses'] = [response.replace("user_name", user_name) for response in tg['responses']]
                    print(random.choice(tg['responses']))

                # if user wants to login
                elif tag == "login":
                    if user_name:
                        print(f'Iris: You are already logged in as {user_name}!')
                        break
                    name = input("Enter your username(You can type 'cancel' to exit):")
                    if name.lower() == "cancel":
                        print("Iris: Process cancelled by the user")
                        break
                    password = input("Enter your password: ")
                    if authenticate(name, password):
                        user_name = name
                        print(f'Iris: Welcome back, {user_name}')
                    break

                # if user wants to check the status of their application
                elif tag == "check_status":
                    if not user_name:
                        print("Iris: Please login before you can continue")
                        break
                    get_status(user_name)

                else:
                    # for all other tags
                    if tg['login_required'] is True and user_name is None:
                        print("Iris: Please login to continue")
                        break
                    responses = tg['responses']
                    print("Iris: " + random.choice(responses))
                    # content tracking for confirmations
                    if tg['context']:
                        current_context = tg['context']
                    else:
                        current_context = None

    return
