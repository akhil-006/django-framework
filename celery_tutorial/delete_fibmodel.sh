#!/bin/sh

rm *.sqli*; rm -rf fib/migrations

python manage.py makemigrations fib && python manage.py migrate && python manage.py runserver

