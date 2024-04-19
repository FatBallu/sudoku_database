class Solution(object):
    def solveSudoku(self, board):
        for row in range(9):
            for col in range(9):
                strboard = str(board[row][col])
                if strboard == '.':
                    # cast str() on num by map()
                    for num in map(str, range(1, 10)):  
                        if self.is_valid(board, row, col, num):
                            board[row][col] = num
                            if self.solveSudoku(board):
                                return True
                            board[row][col] = '.'
                    return False
        return True

    # num is assumed to be str type
    # example inputs are all strings
    # scan the existing numbers on board
    # only true if no duplicated num
    def is_valid(self, board, row, col, num):
        # Scan row (i)
        for i in range(9):
            if board[row][i] == num:
                return False

        # Scan column (j)
        for i in range(9):
            if board[i][col] == num:
                return False

        # Scan 3x3 box
        box_row = row - row % 3
        box_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if board[i + box_row][j + box_col] == num:
                    return False
        return True

    # if (solveSudoku(board)):
    #     for i in board:
    #         print(i)
    # else:
    #     print("No solution exists")