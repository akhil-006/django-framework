#!/bin/sh

source ~/learning/venv/bin/activate

cd celery_tutorial

flake8 *.py & (isort *.py && black *.py)

cd ../fib

flake8 *.py & (isort *.py && black *.py)

cd ~

deactivate

