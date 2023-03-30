from math import ceil
from typing import Iterator, TypeVar

T = TypeVar("T")


def chunk_by_cpu_count(iterable: list[T], cpu_count: int) -> Iterator[list[T]]:
    """Yield successive n-sized chunks from l."""
    len_iterable = len(iterable)
    for i in range(0, len_iterable, cpu_count):
        yield iterable[i : i + ceil(len_iterable / cpu_count)]
