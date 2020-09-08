###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.3-buster as builder

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /usr/src/app

# install psycopg2 dependencies
#RUN apt-get update && apt-get install -y postgresql-dev gcc python3-dev musl-dev
# install dependencies for pycups
RUN apt-get update &&  apt-get install -y cups gcc libcups2-dev
RUN service cups restart

# lint
RUN pip install --upgrade pip && pip install flake8
COPY . .
#RUN flake8 --ignore=E501,F401 .

# install dependencies
COPY ./requirements.txt .
RUN pip install --upgrade pip && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.3-buster

ENV APP_HOME=/opt/app

# create the app user
RUN useradd app

RUN apt-get update &&  apt-get install -y cups gcc libcups2-dev

# create the appropriate directories
WORKDIR $APP_HOME

# install dependencies
RUN apt-get install -y netcat
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache /wheels/*

RUN /etc/init.d/cups restart

# copy entrypoint-prod.sh
COPY ./entrypoint.sh $APP_HOME

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/opt/app/entrypoint.sh"]
