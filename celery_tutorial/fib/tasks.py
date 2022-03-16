import datetime
import time

from celery_tutorial.celery import app
from .models import FibModel

i = 0
a, b = 0, 1

d = {}


def clear_cache():
    global a, b, i, d
    a, b = 0, 1
    i = 0
    d.clear()


def fib_seq(n):
    # 0,1,1,2,3,5,8,13,21,34,55,89,144
    global a, b, i
    d[i], d[i + 1] = a, b

    if i == n:
        return d[i]
    else:
        i += 1
    a, b = b, a + b

    return fib_seq(n)


@app.task(bind=True)
def fib_task(self, id_val):
    fib = FibModel.objects.filter(input__exact=id_val)
    try:
        fib.create(output=str(fib_seq(id_val)), status='success', date_modified=datetime.datetime.now()) if not list(fib) else \
            fib.update(output=str(fib_seq(id_val)), status='success', date_modified=datetime.datetime.now())
    except Exception as ex:
        fib.update(output=ex.__str__(), status='error', date_modified=datetime.datetime.now())
    clear_cache()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
