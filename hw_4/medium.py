import math
from threading import Lock
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from easy import time_it


def partial_sum(f, a, iters, step):
    local_acc = 0
    for i in range(iters):
        local_acc += f(a + i * step) * step
    return local_acc


@time_it
def integrate(f, a, b, *, pool_type, n_jobs=1, n_iter=100000000):
    acc = 0
    step = (b - a) / n_iter
    integrate_lock = Lock()

    f_l = [f] * n_jobs
    iters_per_job = n_iter // n_jobs
    iters_l = [iters_per_job + 1] * (n_iter % n_jobs) + [iters_per_job] * (n_jobs - n_iter % n_jobs)
    a_l = []
    s = 0
    for it in iters_l:
        a_l.append(a + (b - a) * (s / n_iter))
        s += it

    step_l = [step] * n_jobs

    with pool_type(n_jobs) as pool:

        l = pool.map(partial_sum, f_l, a_l, iters_l, step_l)
            # if not i % 50:
            #     print(i)
        acc = sum(l)

    return acc


if __name__ == '__main__':
    with open('artifacts/medium_timing.txt', 'w') as f:
        for threads_n in range(1, 17):
            result = integrate(math.cos, 0, math.pi / 2, pool_type=ThreadPoolExecutor, n_jobs=threads_n)
            f.write(f'{threads_n} threads: {result[0]} s, result={result[1]}\n')

        f.write('\n')

        for processes_n in range(1, 17):
            result = integrate(math.cos, 0, math.pi / 2, pool_type=ProcessPoolExecutor, n_jobs=processes_n)
            f.write(f'{processes_n} processes: {result[0]} s, result={result[1]}\n')
