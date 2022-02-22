from easy import Matrix


class HashedMatrix(Matrix):
    __hashed_values = dict()

    def __hash__(self): # :(
        modulo = 10 ** 18 + 3
        s = 0
        for row in self:
            for x in row:
                s = (s + pow(2, int(x), modulo)) % modulo

        return s

    def __matmul__(self, other):
        key = hash((self, other))
        if key not in self.__hashed_values:
            self.__hashed_values[key] = HashedMatrix(super().__matmul__(other))

        return self.__hashed_values[key]
