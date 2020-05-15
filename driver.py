# Implementation of an optimised back-tracking search algorithm for solving 9x9 Sudoku
# Written by: Intsar Saeed

import re
import sys


class Solver(object):

    def __init__(self, output_file=None, raw_data=None):
        self.raw_data = list(raw_data)
        self.sudoku_board = {}
        self.file = output_file
        self.row_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}
        self.row_group = [['A', 'B', 'C'], ['D', 'E', 'F'], ['G', 'H', 'I']]
        self.col_group = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

    def fill_board(self):
        """ This method fills the values into the sudoku board """
        slope = 0
        for i in range(0, len(self.row_map.keys())):
            for j in range(0, len(self.row_map.keys())):
                key = self.row_map[i + 1] + str(j + 1)
                value = int(self.raw_data[j + (8 * i + slope)])
                self.sudoku_board.update({key: value})
            slope += 1

    def print_board(self, board):
        """This method prints the input board in a nice format on console"""

        for i in range(0, len(self.row_map.keys())):
            for j in range(0, len(self.row_map.keys())):
                print(" | {:>2}".format(board[self.row_map[i + 1] + str(j + 1)]), end='')
            print("\n")
        print(" --------------------- ")

    def solve_board(self):
        """This method call the back-tracking algorithm for solving the Sudoku"""

        self.fill_board()

        if self.bts_solver():
            for i in self.sudoku_board.keys():
                self.file.write(str(self.sudoku_board[i]))
            self.file.write(" BTS")
            print("Solution Found!")

    def find_zero(self):
        """ This method try to find the zero (empty space) in Sudoku board and return the dictionary key """

        for key, val in self.sudoku_board.items():
            if val == 0:
                return key
        return ""

    def is_valid(self, board, position, value) -> bool:
        """ This method checks if the inserted value at a position is a valid value """

        row_loc = re.findall(r'\w+', position)[0][0]  # Alphabet
        col_loc = re.findall(r'\w+', position)[0][1]  # Number

        for i in range(0, 9):
            if (board[row_loc + str(i+1)] == value) or (board[self.row_map[i+1] + col_loc] == value):
                return False

        r_grp, c_grp = [], []
        for i in range(3):
            if row_loc in self.row_group[i]:
                r_grp = (self.row_group[i])
            if int(col_loc) in self.col_group[i]:
                c_grp = (self.col_group[i])

        constraint = set([self.sudoku_board[r + str(c)] for r in r_grp for c in c_grp])
        if value in constraint:
            return False
        return True

    def bts_solver(self) -> bool:
        """ This method finds the backtracking solution of the given Sudoku board"""
        empty_position = self.find_zero()
        if empty_position == "":
            self.print_board(self.sudoku_board)
            return True

        for value in range(1, 10):
            if self.is_valid(self.sudoku_board, empty_position, value):
                self.sudoku_board[empty_position] = value
                if self.bts_solver():
                    return True
                self.sudoku_board[empty_position] = 0
        return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():

    input_board = sys.argv[1]
    output_file = "output.txt"
    f = open(output_file, 'w')

    # Load the data
    sudoku_solver = Solver(output_file=f, raw_data=input_board)
    sudoku_solver.solve_board()

    # close file
    f.close()


if __name__ == '__main__':
    main()
