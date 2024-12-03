from tinydb import TinyDB, Query
import random

db = TinyDB("application_data.json")
query = Query()
app_status = ['Accepted', 'Rejected', 'Pending']    # assigns a random status to applications from one of these


# applying for new card
def new_application(name, card_type):
    try:
        if not name.isdigit():
            if db.search(query.name == str(name)):
                print(f'Iris: Sorry {name}, it seems like you already have an active application. You may only have '
                      f'one active application')
                return
            # Generates a 6 digit unique ID
            while True:
                unique_id = random.randint(100000, 999999)
                # Check if this ID already exists
                if not db.search(query.id == unique_id):
                    break
            db.insert({'id': unique_id, 'name': name, 'card_type': card_type, 'status': random.choice(app_status)})
            print(f'Iris: Your application has been sent with the application number {unique_id}')
        else:
            print('Iris: Sorry, An unexpected error occurred. Please try again.')

        return
    except Exception as e:
        print(f'Iris: An error occurred: {e}')


# check status of application
def get_status(name):
    try:
        # if name is number
        if not name.isdigit():
            result = db.search(query.name == str(name))
            if result:
                result = result[0]
        else:
            print('Iris: Sorry, An unexpected error occurred. Please try again.')
            return

        # if there is a match
        if result:
            res_id = result['id']
            status = result['status']

            print(f'Iris: The status of your application with id {res_id} is {status}')
        else:
            print(f'Iris: I could not find any application(s) under your name, {name}. Please try again.')

        return
    except Exception as e:
        print(f'An error occurred: {e}')


# withdrawing active applications
def withdraw_application(name):
    try:
        if not name.isdigit():
            current = db.search(query.name == str(name))
            if current:
                res_id = current[0]['id']
                # Proceed to remove the entry if the user confirms
                result = db.remove(query.name == str(name))
                if result:
                    print(f'Iris: Application with ID {res_id} has been successfully withdrawn.')
                else:
                    print("Iris: Error: Unable to withdraw the application.")
            else:
                print(f'Iris: I could not find any application under your name, {name}.')

        return
    except Exception as e:
        print(f'Iris: An error occurred: {e}')
