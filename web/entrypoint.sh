#!/bin/sh

if [ "$CHECK_DATABASE" = "true" ]; then
    echo "Waiting for $DB_HOST:$DB_PORT..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "DB started"
fi

# Make migrations and migrate the database.
echo "Migrating the database."
python manage.py migrate --noinput
python manage.py collectstatic --noinput

/etc/init.d/cups restart
/usr/sbin/lpadmin -p $PRINTER_NAME -v $PRINTER_CUPS_URL -L barraka -E

exec "$@"
