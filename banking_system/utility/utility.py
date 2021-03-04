from django.utils import timezone


def get_time():
    return timezone.now()


def datetime_to_epoch(date_time):

    if date_time:
        date_time = int(date_time.strftime("%s"))
    return date_time
