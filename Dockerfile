FROM python:3.6-stretch
WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=config.settings.production \
    WEB_CONCURRENCY=3

RUN apt-get update -y && \
    apt-get install -y libsm6 libxext6 libxrender-dev

# Install Python requirements.
COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR .
#Install EmoPy
RUN git clone https://github.com/thoughtworksarts/EmoPy.git
COPY /fermodel.py /EmoPy/EmoPy/src
COPY /EmoPy/EmoPy /
WORKDIR /app
# Copy application code.
COPY . .

ENV DJANGO_DB_NAME=d4rgmcmifs0odk
ENV DJANGO_SU_NAME=rlrlzzofsuoold
ENV DJANGO_SU_EMAIL=strongamil998@gmail.com
ENV DJANGO_SU_PASSWORD=0d3cc208ae04dd72bf40dfcaf92b8372ed0d52ea2eede2496f39c27e24eb5500

RUN python manage.py migrate

#RUN python -c "import django; django.setup(); from django.contrib.auth.models import User; \
#                  User.objects.create_superuser('emiliya', 'strongamil1998@gmail.com', '123')"

#               "import django; django.setup(); \
#   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
#   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
#   username='$DJANGO_SU_NAME', \
#   email='$DJANGO_SU_EMAIL', \
#   password='$DJANGO_SU_PASSWORD')"

RUN python manage.py collectstatic --noinput --clear && \
    python manage.py makemigrations && \
    python manage.py migrate



# Run application
CMD gunicorn CloudAndGridREC.wsgi --preload --bind 0.0.0.0:$PORT --timeout 500 --max-requests 12