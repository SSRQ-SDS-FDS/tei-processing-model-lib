from math import ceil
from typing import Iterator, TypeVar

T = TypeVar("T")


def chunk_by_cpu_count(iterable: list[T], cpu_count: int) -> Iterator[list[T]]:
    """Yield successive n-sized chunks from l."""
    len_iterable = len(iterable)
    chunk_size = ceil(len_iterable / cpu_count)
    for i in range(0, len_iterable, chunk_size):
        yield iterable[i : i + chunk_size]
