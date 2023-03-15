FROM python:3.10-slim AS build
MAINTAINER KYLN24 <kyln24@fduhole.com>

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt

FROM python:3.10-slim
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY . /app

CMD ["python", "/app/main.py"]
