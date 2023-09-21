import os
from datetime import datetime
from uuid import uuid4
from functools import partial


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
