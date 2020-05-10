# Linear regression with multiple features using gradient decent
# The script will stop after itr number of iterations
# Written by: Intsar Saeed

import re
import sys
import numpy as np


class Solver(object):

    def __init__(self, output_file=None, raw_data=None):
        self.raw_data = list(raw_data)
        self.file = output_file
        self.sudoku_board = {}
        self.sudoku_board_solved = {}
        self.row_map = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H', 9: 'I'}

    def fill_board(self):
        """ This method fills the values into the sudoku board """
        slope = 0
        for i in range(0, len(self.row_map.keys())):
            for j in range(0, len(self.row_map.keys())):
                key = self.row_map[i + 1] + str(j + 1)
                value = int(self.raw_data[j + (8 * i + slope)])  # index the input string values here!
                self.sudoku_board.update({key: value})
            slope += 1
        print("The initial Sudoku Board = ")
        self.print_board(self.sudoku_board)


    def ac3_solver(self):

        return False

    def solve_board(self):
        """This method try to solve the Sudoku using back-tracking and AC3"""
        self.fill_board()  # fill the board with the initial data
        print("Solving using BTS ... ")

        if self.bts_solver():
            for i in self.sudoku_board.keys():
                self.file.write(str(self.sudoku_board[i]))
            self.file.write(" BTS")
            print("solved using BTS")

        #self.fill_board()  # fill the board again with the initial data
        #print("Solving using AC3 ... ")

        # if self.ac3_solver():
        #     return "solved using ac3"

    def print_board(self, board):
        for i in range(0, len(self.row_map.keys())):
            for j in range(0, len(self.row_map.keys())):
                print(" | {:>2}".format(board[self.row_map[i + 1] + str(j + 1)]), end='')
            print("\n")
        print(" ---------------------- ")

    def find_zero(self) -> str:
        """ This method try to find the zero (empty space) in Sudoku board and return the dictionary key """
        for i in range(0, len(self.row_map.keys())):
            for j in range(0, len(self.row_map.keys())):
                if self.sudoku_board[self.row_map[i + 1] + str(j + 1)] == 0:
                    return self.row_map[i + 1] + str(j + 1)
        return ""

    def is_valid(self, board, position, value) -> bool:
        """ This method checks if the inserted value at a position is a valid value """

        # Get row and column
        row = re.findall(r'\w+\d+', position)[0][0]  # Alphabet
        col = int(re.findall(r'\w+\d+', position)[0][1])  # Number

        # Row validity
        for i in range(1, 10):
            if (board[row + str(i)] == value) and (row + str(i) != position) and (board[row + str(i)] != 0):
                return False

        # Column validity
        for i in range(0, len(self.row_map.keys())):
            if (board[self.row_map[i + 1] + str(col)] == value) and (row + str(i+1) != position) and (board[row + str(i + 1)] != 0):
                return False

        # Box validity
        if col <= 3:
            range_to_check = [0, 3]
        elif col >= 7:
            range_to_check = [6, 9]
        else:
            range_to_check = [3, 6]

        if row == "A" or row == "B" or row == "C":
            for i in range(range_to_check[0], range_to_check[1]):
                if (board["A" + str(i + 1)] == value) and ("A" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["B" + str(i + 1)] == value) and ("B" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["C" + str(i + 1)] == value) and ("C" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False

        elif row == "D" or row == "E" or row == "F":
            for i in range(range_to_check[0], range_to_check[1]):
                if (board["D" + str(i + 1)] == value) and ("D" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["E" + str(i + 1)] == value) and ("F" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["F" + str(i + 1)] == value) and ("F" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
        else:
            for i in range(range_to_check[0], range_to_check[1]):
                if (board["G" + str(i + 1)] == value) and ("G" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["H" + str(i + 1)] == value) and ("H" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
                if (board["I" + str(i + 1)] == value) and ("I" + str(i + 1) != position) and (board[row + str(i+1)] != 0):
                    return False
        return True

    def bts_solver(self) -> bool:
        """ This method finds the backtracking solution of the given Sudoku board"""
        zero_position = self.find_zero()
        # # Get row and column
        # row = re.findall(r'\w+\d+', zero_position)[0][0]  # Alphabet
        # col = int(re.findall(r'\w+\d+', zero_position)[0][1])  # Number

        if zero_position == "":
            self.print_board(self.sudoku_board)
            return True

        for value in range(1, 10):
            if self.is_valid(self.sudoku_board, zero_position, value):
                self.sudoku_board[zero_position] = value
                if self.bts_solver():
                    return True
                self.sudoku_board[zero_position] = 0
        return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    input_board = sys.argv[1]
    output_file = "output.txt"
    f = open(output_file, 'w')
    # Read the data
    # age in years, weight in KG, height in meters
    # data = pd.read_csv(input_file, header=0)

    # Load the data
    sudoku_solver = Solver(output_file=f, raw_data=input_board)
    sudoku_solver.solve_board()

    # Close the file
    print("Completed")


if __name__ == '__main__':
    main()
