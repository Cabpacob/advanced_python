from multiprocessing import Pool

def calc(value):
    return value ** 2

def calc_parallel(values):

    p = Pool(processes=2)
    return p.map(calc, values)

r = calc_parallel([1, 2, 3, 4])
print(r)
