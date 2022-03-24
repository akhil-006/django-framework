#!/bin/sh

source ~/learning/venv/bin/activate

cd celery_tutorial

flake8 *.py & (isort *.py && black *.py)

cd ../fib

echo "PWD:: " $PWD

flake8 *.py & (isort *.py && black *.py)

cd ../authenticate_authorization_app

echo "PWD:: " $PWD

flake8 *.py & (isort *.py && black *.py)

cd ~

deactivate

