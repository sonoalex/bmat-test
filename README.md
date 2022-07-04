# BMAT TEST

The test provided by Bmat team.

## Installation

Docker needed.
Python3 and requests module installed on your machine.

```bash
docker-compose build
docker-compose up -d
```

## Init Celery Worker

```bash
docker-compose run --rm app sh -c "celery -A app worker --loglevel=info"
```

## Test API Endpoint 1

```bash
# From your local machine, execute
python3  test_upload.py
# This will PUT test_upload.csv to the server using the endpoint: /task/upload/<filename>
# Response:
{'task_status': 'PENDING', 'task_id': '422a6acf-497a-40b5-aeed-e50a88063d59'}

```

## Test API Endpoint 2

```bash
# Go to the browser and go to
http://127.0.0.1:8000/task/422a6acf-497a-40b5-aeed-e50a88063d59/
# This will return:
{'task_status': 'PENDING', 'task_id': '422a6acf-497a-40b5-aeed-e50a88063d59'}
#if PENDING OR FAILED
# Or will download the new generated file if task_status is SUCCESS.

```

## Extra
- Django framework
- PostgreSQL
- Redis
- Celery

