FROM python:3.10

ENV APP_HOME=/app
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR $APP_HOME

COPY TaskTracker/requirements.txt $APP_HOME

RUN pip install --upgrade --no-cache-dir pip wheel setuptools \
    && pip install --no-cache-dir --upgrade -r requirements.txt

COPY TaskTracker/.env $APP_HOME

WORKDIR $APP_HOME
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8880", "--log-level",  "debug", "src.main:app"]

EXPOSE 8880
