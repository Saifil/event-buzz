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

def generate_bert_input():
    # output_txt_file = open("output/input.txt", "a")
    output_txt_file = open("output/input_distinct.txt", "a")

    # event_list = svc.get_all_event_data()
    event_list = svc.get_unique_descriptions()
    for event in event_list:
        # output_txt_file.write(event.description + "\n")
        output_txt_file.write(event + "\n")
        # print(event)
    output_txt_file.close()


# def create_multiple_users():
#     user_document_list = [User("AAA", "123", "aaa@mail.com"), User("BBB", "456", "bbb@mail.com"),
#                           User("CCC", "789", "ccc@mail.com"), User("DDD", "101", "ddd@mail.com")]
#     usrs = svc.create_multiple_users(user_document_list)

def get_events_by_clusters():
    for cluster_number in range(50):
        file = open("output/clusters/cluster_db/cluster_" + str(cluster_number) + ".txt", 'a+')
        print(f"Cluster number: {cluster_number}")

        event_list_clstr = svc.get_events_by_clusters(cluster_number)
        for event in event_list_clstr:
            file.write(event.description + "\n")

        file.close()


def make_cluster_collection():
    for i in range(50):
        cluster_count = svc.get_cluster_counts(i)
        cluster_name = "dummy_name"
        clstr = svc.create_new_cluster(i, cluster_name, cluster_count)

def main():
    mongo_setup.global_init()  # Connect to the db

    if state.active_account is None:
        print("No active session")

    # scrape.save_to_csv()

    # Login-signup
    # create_new_user()
    # user_login()  # login the user

    # if state.active_account is not None:
    #     print(f"Active session {state.active_account}")

    # generate_bert_input()

    # get_events_by_clusters()

    # make_cluster_collection()
    # get_all_event_data()
    # event_list = svc.get_event_by_cluster_limit()

    return 0


if __name__ == "__main__":
    main()
