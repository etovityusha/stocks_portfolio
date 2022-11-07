from datetime import time

from domain.base import BaseEntity


class Exchange(BaseEntity):
    title: str
    suffix: str

    utc_offset: int | None = None
    working_start: time | None = None
    working_end: time | None = None
