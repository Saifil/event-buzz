import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc
import database.infrastructure.state as state

# Test multiple record insertion
from database.data.user import User
import scrape


# Signup
def create_new_user():
    print("==================Please enter you details=================")

    name = input("Enter your name\n")
    email = input("Enter your email\n")
    password = input("Enter your password\n")
    age = int(input("Enter your age\n"))

    educ = input("Enter your education\n")
    major = input("Enter your major\n")

    state.active_account = svc.create_new_user(name, email, password, age, educ, major)

# Login
def user_login():
    print("==================Please enter you Credentials=================")

    email = input("Enter your email\n")
    password = input("Enter your password\n")

    query_user = svc.get_user_info(email, password)
    if query_user is not None:
        print(f"User with name {query_user.name} Logged In.")
    else:
        print("Invalid credentials.")


def get_all_event_data():
    event_list = svc.get_all_event_data()
    for event in event_list[:5]:
        print(f"Event name: {event.title}")


# def create_multiple_users():
#     user_document_list = [User("AAA", "123", "aaa@mail.com"), User("BBB", "456", "bbb@mail.com"),
#                           User("CCC", "789", "ccc@mail.com"), User("DDD", "101", "ddd@mail.com")]
#     usrs = svc.create_multiple_users(user_document_list)

def main():
    mongo_setup.global_init()  # Connect to the db

    if state.active_account is None:
        print("No active session")

    # scrape.save_to_csv()

    # Login-signup
    # create_new_user()
    # user_login()  # login the user

    if state.active_account is not None:
        print(f"Active session {state.active_account}")

    get_all_event_data()

    return 0


if __name__ == "__main__":
    main()
