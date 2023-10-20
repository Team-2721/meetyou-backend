from django.utils import timezone
from dateutil.relativedelta import relativedelta
from datetime import datetime
from uuid import uuid4
from functools import partial
import os
import random
import string


def _update_filename(instance, filename, path, hash):
    ymd_path = datetime.now().strftime("%Y/%m/%d")
    path = f"{path}/{ymd_path}"
    if hash:
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"
    filename = filename

    return os.path.join(path, filename)


def upload_to(path, hash):
    return partial(_update_filename, path=path, hash=hash)


def now_minus_hour_result(hour):
    return timezone.localtime(timezone.now()) - relativedelta(hours=hour)


def get_room_code():
    code = ""
    for _ in range(4):
        code += random.choice(string.digits)
    return code
