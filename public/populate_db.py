import scrape
from datetime import datetime

import database.data.mongo_setup as mongo_setup
import database.services.data_service as svc
import database.infrastructure.state as state

from database.data.event import Event

def insert_events():
    # keys = ["title", "description", "category", "location", "image_url", "related_link", "st_date", "end_date",
    #         "st_time", "end_time"]

    event_document_list = []

    event_list = scrape.scrape_events()  # Scrape web for event dataset
    for event in event_list[1:]:
        print(event)
        # To datetime: 'Saturday, August 31, 2019'
        event[6] = datetime.strptime(event[6], '%A, %B %d, %Y')
        event[7] = datetime.strptime(event[7], '%A, %B %d, %Y')

        # Get hours + mins in int mins
        event[8] = int(event[8].split(":")[0]) * 60 + int(event[8].split(":")[1])  # st_time
        event[9] = int(event[9].split(":")[0]) * 60 + int(event[9].split(":")[1])  # end_time

        # # get the object for each event
        event_document_list.append(Event(event[0], event[1], event[2], event[3],
                                         event[4], event[5], event[6], event[7], event[8], event[9]))
    # print(event_document_list)
    ret = svc.insert_events(event_document_list)
    if not ret:
        print(f"Error while pushing the values in the collection.")
    else:
        print(f"Successfully inserted {len(ret)} event entries into the event collection")


def main():
    mongo_setup.global_init()  # Connect to the db
    insert_events()


if __name__ == '__main__':
    main()
