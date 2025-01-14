class Matrix:
    def __init__(self, rows, cols):
        # Initializes a matrix with the specified number of rows and columns, filled with zeros.
        if not isinstance(rows, int) or rows <= 0:
            raise ValueError("Number of rows must be a positive integer.")
        if not isinstance(cols, int) or cols <= 0:
            raise ValueError("Number of columns must be a positive integer.")
        self.matrix = [[0 for _ in range(cols)] for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    def insertCol(self, col_index, col_data):
        # Inserts a new column with the given data at the specified column index.
        # Raises ValueError if the column index is out of bounds or if the column data length
        # does not match the number of rows.
        if not isinstance(col_index, int) or not (0 <= col_index <= self.cols):
            raise ValueError("Column index is out of bounds.")
        if not isinstance(col_data, list) or len(col_data) != self.rows:
            raise ValueError("Column data must be a list with a length equal to the number of rows.")

        for i in range(self.rows):
            self.matrix[i].insert(col_index, col_data[i])
        self.cols += 1