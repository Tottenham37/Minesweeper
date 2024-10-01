import numpy as np

class Math_lib:
    def __init__(self, rows, columns, mines):
        self.rows = rows
        self.columns = columns
        self.mines = mines
        self.field = np.zeros((self.rows, self.columns))
        indices = np.random.choice(self.rows * self.columns, size=self.mines, replace=False)
        row_indices, col_indices = np.unravel_index(indices, (self.rows, self.columns))
        self.field[row_indices, col_indices] = -1

    def calculate_mines(self, i, j):
        counter = 0
        for k in range(-1, 2):
            for l in range(-1, 2):
                if k == 0 and l == 0:
                    continue
                if 0 <= i+k < self.rows and 0 <= j+l < self.columns:
                    if self.field[i+k, j+l] == -1:
                        counter += 1

        return counter









