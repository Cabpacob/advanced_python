import numpy as np
import numbers


class MatrixFileSaverMixin:
    def write_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write(str(self))


class MatrixIterMixin:
    def __iter__(self):
        return iter(self._matrix)


class MatrixStrMixin(MatrixIterMixin):
    def __str__(self):
        return '[\n\t' + '\n\t'.join(map(str, self)) + '\n]'


class MatrixSizeCheckerMixin:
    @staticmethod
    def check_size(matrix):
        rows = len(matrix)
        columns = len(matrix[0])

        def equal_len(row):
            return len(row) == columns

        if not all(map(equal_len, matrix)):
            raise KeyError(f'wrong table with {columns} columns and {rows} rows')


class MatrixPropertiesMixin:
    @property
    def rows(self):
        return self.__rows

    @property
    def columns(self):
        return self.__columns

    @property
    def T(self):
        return Matrix(zip(*self._matrix))


class MatrixDataGetterSetterMixin(MatrixSizeCheckerMixin, MatrixPropertiesMixin):
    def __init__(self, matrix):
        self.check_size(matrix)

        self._matrix = matrix
        self.__rows = len(self._matrix)
        self.__columns = len(self._matrix[0])

    @property
    def matrix(self):
        return self._matrix

    @matrix.setter
    def matrix(self, new_matrix):
        self.check_size(new_matrix)

        self._matrix = new_matrix
        self.__rows = len(self._matrix)
        self.__columns = len(self._matrix[0])


class Matrix(np.lib.mixins.NDArrayOperatorsMixin, MatrixFileSaverMixin, MatrixStrMixin, MatrixDataGetterSetterMixin):
    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get('out', ())
        for x in inputs + out:
            # Only support operations with instances of _HANDLED_TYPES.
            # Use ArrayLike instead of type(self) for isinstance to
            # allow subclasses that don't override __array_ufunc__ to
            # handle ArrayLike objects.
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        # Defer to the implementation of the ufunc on unwrapped values.
        inputs = tuple(x.matrix if isinstance(x, Matrix) else x
                       for x in inputs)
        if out:
            kwargs['out'] = tuple(
                x.value if isinstance(x, Matrix) else x
                for x in out)
        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            # multiple return values
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            # no return value
            return None
        else:
            # one return value
            return type(self)(result)
