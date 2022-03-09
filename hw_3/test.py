import numpy as np
import easy
import medium
import hard


def gen_easy_artifacts(matrix_1, matrix_2):
    easy_m1 = easy.Matrix(matrix_1)
    easy_m2 = easy.Matrix(matrix_2)

    with open('artifacts/easy/matrix+.txt', 'w') as f:
        f.write(str(easy_m1 + easy_m2))

    with open('artifacts/easy/matrix*.txt', 'w') as f:
        f.write(str(easy_m1 * easy_m2))

    with open('artifacts/easy/matrix@.txt', 'w') as f:
        f.write(str(easy_m1 @ easy_m2))


def gen_medium_artifacts(matrix_1, matrix_2):
    easy_m1 = medium.Matrix(matrix_1)
    easy_m2 = medium.Matrix(matrix_2)

    with open('artifacts/medium/matrix+.txt', 'w') as f:
        f.write(str(easy_m1 + easy_m2))

    with open('artifacts/medium/matrix*.txt', 'w') as f:
        f.write(str(easy_m1 * easy_m2))

    with open('artifacts/medium/matrix@.txt', 'w') as f:
        f.write(str(easy_m1 @ easy_m2))


def gen_hard_artifacts():
    while True:
        A = hard.HashedMatrix(np.random.randint(0, 10, (3, 3)))
        B = hard.HashedMatrix(np.random.randint(0, 10, (3, 3)))

        C = hard.HashedMatrix(np.random.randint(0, 10, (3, 3)))
        D = B

        AB = A @ B
        CD = easy.Matrix(C) @ easy.Matrix(D)

        if (hash(A) == hash(C)) and (A != C) and (B == D) and (AB != CD):
            with open('artifacts/hard/A.txt', 'w') as f:
                f.write(str(A))

            with open('artifacts/hard/B.txt', 'w') as f:
                f.write(str(B))

            with open('artifacts/hard/C.txt', 'w') as f:
                f.write(str(C))

            with open('artifacts/hard/D.txt', 'w') as f:
                f.write(str(D))

            with open('artifacts/hard/AB.txt', 'w') as f:
                f.write(str(A @ B))

            with open('artifacts/hard/CD.txt', 'w') as f:
                f.write(str(easy.Matrix(C) @ easy.Matrix(D)))

            with open('artifacts/hard/hash.txt', 'w') as f:
                f.write(str(hash(A @ B)))

                f.write(str(hash(hard.HashedMatrix(easy.Matrix(C) @ easy.Matrix(D)))))

            break


if __name__ == '__main__':
    np.random.seed(0)

    matrix_1 = np.random.randint(0, 10, (10, 10))
    matrix_2 = np.random.randint(0, 10, (10, 10))

    gen_easy_artifacts(matrix_1, matrix_2)
    gen_medium_artifacts(matrix_1, matrix_2)
    gen_hard_artifacts()
