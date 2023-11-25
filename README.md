# Retention Updater

Asynchronously sends retention directory and day offset csv data to REST API endpoint.

## Assumptions

- Always two values per row

- Any directories containing the delimiter character are enclosed in double quotes

- Day offset is either a valid integer or blank - blank becomes 0

- POST requests

- Endpoint can handle 100 concurrent requests

- Endpoint can handle directory format(s) in file (differences between UNIX and Windows)

## Run

Install Python (3.10 or greater)

Install dependencies:

`python -m pip install -r requirements.txt`

Run client:

`python main.py`

Run test server (hosted at `http://localhost:8080/retention`):

`python test_server.py`