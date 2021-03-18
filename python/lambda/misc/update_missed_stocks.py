from datetime import timedelta, date
import time
import requests


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


start_date = date(2021, 1, 5)
end_date = date(2021, 3, 15)
for single_date in daterange(start_date, end_date):
    print(single_date.strftime("%Y-%m-%d"))
    response = requests.post(
        "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/stocks/NYSE/TAN/{}".format(
            single_date.strftime("%Y-%m-%d")
        )
    )
    print(response.status_code)
    time.sleep(5)
    response = requests.post(
        "https://g4spmx84mk.execute-api.ap-southeast-2.amazonaws.com/stocks/NYSE/VOO/{}".format(
            single_date.strftime("%Y-%m-%d")
        )
    )
    print(response.status_code)
    time.sleep(5)
