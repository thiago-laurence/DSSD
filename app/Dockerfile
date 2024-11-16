# syntax=docker/dockerfile:1
FROM python:3.12

COPY . /code/

WORKDIR /code

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x ./entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]