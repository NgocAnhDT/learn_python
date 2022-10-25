import datetime
from app.models import *
from celery import shared_task
from dateutil.relativedelta import relativedelta


@shared_task(name="add")
def add(x, y):
    return x + y


@shared_task(name="abc")
def abc(x, y):
    return x * y


@shared_task(name="xsum")
def xsum(numbers):
    return sum(numbers)


@shared_task(name="count_user")
def count_user():
    return User.objects.count()


@shared_task(name="rename_user")
def rename_user(user_id, name):
    user = User.objects.get(id=user_id)
    user.first_name = name
    user.save()


@shared_task(name="update_status")
def update_status():
    insurances = Insurance.objects.all()
    for insurance in insurances:
        date_expired = insurance.date_of_purchase + relativedelta(months=+insurance.warranty_period)
        if date_expired < datetime.now().date():
            insurance.status = 'ex'
            insurance.save()
    return 'Update success'

