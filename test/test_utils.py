from multiprocessing import cpu_count

from src.utils import chunk_by_cpu_count


def test_chunk_by_cpu_count():
    cpus = cpu_count()
    full_list = [i for i in range(10 * cpus)]
    chunked_list = [x for x in chunk_by_cpu_count(full_list, cpu_count())]
    assert len(chunked_list) == cpus
    for i in chunked_list:
        assert len(i) == 10
