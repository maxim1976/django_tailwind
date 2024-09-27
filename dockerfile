FROM python:3.11-bullseye

# Set environment variables
ENV PYTHONBUFFERED=1

WORKDIR /django_tailwind

COPY requirements.txt /django_tailwind/

RUN pip3 install -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000