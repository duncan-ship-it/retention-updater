# Retention Updater

Asynchronously sends csv data retention directory and day offset data to REST API endpoint.

Assumptions:

- Two values per row

- Day offset is either a valid decimal or blank - any decimals are floored to integers in the request

- JSON request (POST)

- Endpoint can handle 100 concurrent requests

Install dependencies (Python >=3.10):

`python -m pip install -r requirements.txt`

Run client:

`python main.py`

Run test server (hosted at `http://localhost:8080/retention`):

`python test_server.py`