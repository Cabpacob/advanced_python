from functools import reduce


class Vector:
    def __init__(self, vector):
        self.__vector = list(vector)
        self.__length = len(self.__vector)

    def __len__(self):
        return self.__length

    def __iter__(self):
        return iter(self.__vector)

    def __getitem__(self, key):
        return self.__vector[key]

    def __setitem__(self, key, value):
        self.__vector[key] = value

    def __add__(self, other):
        return Vector(map(lambda x, y: x + y, self, other))

    def __mul__(self, other):
        return Vector(map(lambda x, y: x * y, self, other))

    def __matmul__(self, other):
        return reduce(lambda x, y: x + y, self * other)

    def __str__(self):
        return '[' + ', '.join(map(str, self.__vector)) + ']'

    def __eq__(self, other):
        return list(self) == list(other)


class Matrix:
    def __init__(self, matrix):
        self.__matrix = [Vector(row) for row in matrix]
        self.__rows = len(self.__matrix)
        self.__columns = len(self.__matrix[0])

        def equal_len(row):
            return len(row) == self.__columns

        if not all(map(equal_len, self.__matrix)):
            raise KeyError(f'wrong table with {self.__columns} columns and {self.__rows} rows')

    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def T(self):
        return Matrix(zip(*self.__matrix))

    def __iter__(self):
        return iter(self.__matrix)

    def __getitem__(self, key):
        return self.__matrix[key]

    def __add__(self, other):
        if (self.rows, self.columns) != (other.rows, other.columns):
            raise KeyError(f'Cant add Matrix({self.rows}, {self.columns}) and Matrix({other.rows, other.columns})')

        return Matrix(map(lambda x, y: x + y, self, other))

    def __mul__(self, other):
        if (self.rows, self.columns) != (other.rows, other.columns):
            raise KeyError(f'Cant multiply Matrix({self.rows}, {self.columns}) and Matrix({other.rows, other.columns})')

        return Matrix([x * y for x, y in zip(self, other)])

    def __matmul__(self, other):
        if self.rows != other.columns:
            raise KeyError(f'Cant math multiply Matrix({self.rows}, {self.columns}) and Matrix({other.rows, other.columns})')

        def get_matmul_row(row):
            return Vector([row @ column for column in other.T])

        return Matrix(map(get_matmul_row, self))

    def __str__(self):
        return '[\n\t' + '\n\t'.join(map(str, self)) + '\n]'

    def __eq__(self, other):
        return all(map(lambda x, y: x == y, self, other))
