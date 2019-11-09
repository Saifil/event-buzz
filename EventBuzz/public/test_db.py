import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc
import database.infrastructure.state as state

# Test multiple record insertion
from database.data.user import User


def create_new_user():
    print("==================Please enter you details=================")

    first_name = input("Enter you first name\n")
    last_name = input("Enter you last name\n")
    email = input("Enter you email")

    state.active_account = svc.create_new_user(first_name, last_name, email)
    print()
    print(state.active_account.id)


def create_multiple_users():
    user_document_list = [User("AAA", "123", "aaa@mail.com"), User("BBB", "456", "bbb@mail.com"),
                          User("CCC", "789", "ccc@mail.com"), User("DDD", "101", "ddd@mail.com")]
    usrs = svc.create_multiple_users(user_document_list)


def get_user_info():
    print("==================Please enter user email=================")

    email = input("Enter the email\n")

    query_user = svc.get_user_info(email)
    if query_user:
        print(query_user.first_name)
    else:
        print(f"User with email {email} not found.")


def main():
    mongo_setup.global_init()  # Connect to the db
    # create_new_user()
    # get_user_info()
    create_multiple_users()
    return 0


if __name__ == "__main__":
    main()
