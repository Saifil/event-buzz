import requests
from bs4 import BeautifulSoup
from csv import writer
import time
from datetime import datetime
import sys

FILE_NAME = "gatech_events.csv"
ABSOLUTE_LINK = "https://www.calendar.gatech.edu"

def write_to_csv(row_list):
    output_dir = "db_csv/" + FILE_NAME
    with open(output_dir, "w") as csv_file:
        csv_writer = writer(csv_file)
        csv_writer.writerows(row_list)
        csv_file.close()

def main():
    # To calculate the runtime of the program
    start_time = time.time()

    global FILE_NAME
    if len(sys.argv) > 1:
        FILE_NAME = str(sys.argv[1])

    # Prep the get request
    headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/77.0.3865.90 Mobile Safari/537.36"}
    # url = "https://www.calendar.gatech.edu/events/day/2019-10-01"
    url = "https://www.calendar.gatech.edu/events/day/2019-08-11"  # Aug 11 
    csv_row = [["title", "description", "category", "location", "image_url", "related_link", "st_date", "end_date", "st_time", "end_time"]]

    res = requests.get(url, headers=headers)  # Get the response
    soup = BeautifulSoup(res.text, features="html.parser")  # Get the html page
    event_list = soup.find_all(class_="event")

    i = 1
    month = url.split("-", 3)[1]
    # while month != "01":  # Months till Dec 2019
    while month != "09":  # Month of Aug
        for elem in event_list:
            date = elem.find(class_="date").text
            ttime = elem.find(class_="time").text

            date_column = date.split(" to", 1)
            time_column = ttime.split(" - ", 1)

            st_date = date_column[0].strip()
            end_date = st_date
            if len(date_column) > 1:
                end_date = date_column[1].strip()

            st_time = time_column[0].strip()
            end_time = "11:59 pm"
            if len(time_column) > 1:
                end_time = time_column[1].strip()

            try:
                st_time = datetime.strftime(datetime.strptime(st_time, "%I:%M %p"), "%H:%M")
                end_time = datetime.strftime(datetime.strptime(end_time, "%I:%M %p"), "%H:%M")
            except ValueError:
                st_time = "00:00"
                end_time = "23:59"
                
            cat = ""
            category_list = elem.find(class_="tags")
            if category_list is not None:
                for category in category_list.find_all("a"):
                    cat += category.get_text() + ","
                cat = cat[:-1]

            image_url = elem.find(class_="image-container small-3")
            if image_url is not None:
                image_url = image_url.img['src']
            else:
                image_url = "gatech_logo.png"

            related_link = elem.find("header")
            if related_link is not None:
                related_link = ABSOLUTE_LINK + related_link.a['href']
            else:
                related_link = ""

            csv_row.append([elem.find(class_="small-12 columns info").a.text, elem.find(class_="description").text,
                            cat, elem.find(class_="location").text, image_url, related_link, st_date, end_date, st_time, end_time])

        url = soup.find(title="Navigate to next day")["href"]
        month = url.split("-", 3)[1]
        res = requests.get(url, headers=headers)  # Get the response
        soup = BeautifulSoup(res.text, features="html.parser")  # Get the html page
        event_list = soup.find_all(class_="event")
        print(i, month)
        i = i + 1

    # Debug
    print(csv_row)

    write_to_csv(csv_row)

    print("--Program run time: %s seconds" % round((time.time() - start_time)))


if __name__ == '__main__':
    main()
