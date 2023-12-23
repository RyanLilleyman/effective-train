# Project No: 2
# Author: Ryan Lilleyman
# Description: This is the boggle class that governs the boggle game logic.


import random
import string


class BoggleBoard:
    def __init__(self) -> None:
        """
        Initializes the class instance by setting up the board, seed, and current guess.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        self.__board = [
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
            [" ", " ", " ", " "],
        ]
        self.__seed = None
        self.__current_guess = ""
        self.__guess_list = []

    # Display the Board
    def __str__(self):
        """
        Returns a string representation of the current state of the board.

        This function generates a string representation of the board in a 4x4 grid format.
        Each cell of the grid is filled with the corresponding value from the self.__board
        attribute. The string is formatted using the f-string syntax to dynamically insert
        the values from the board.

        Returns:
            str: A string representation of the current state of the board.
        """
        return f""" 
        +---+ +---+ +---+ +---+
        |{self.__board[0][0]}| |{self.__board[0][1]}| |{self.__board[0][2]}| |{self.__board[0][3]}|
        +---+ +---+ +---+ +---+
        +---+ +---+ +---+ +---+
        |{self.__board[1][0]}| |{self.__board[1][1]}| |{self.__board[1][2]}| |{self.__board[1][3]}|
        +---+ +---+ +---+ +---+
        +---+ +---+ +---+ +---+
        |{self.__board[2][0]}| |{self.__board[2][1]}| |{self.__board[2][2]}| |{self.__board[2][3]}|
        +---+ +---+ +---+ +---+
        +---+ +---+ +---+ +---+
        |{self.__board[3][0]}| |{self.__board[3][1]}| |{self.__board[3][2]}| |{self.__board[3][3]}|
        +---+ +---+ +---+ +---+
        """

    # Some Getters
    def get_board(self):
        """
        Get the board.

        Returns:
            The board.
        """
        return self.__board

    def get_seed(self):
        """
        Get the seed value.

        Returns:
            int: The seed value.
        """
        return self.__seed

    def get_current_guess(self):
        """
        Returns the current guess.

        Returns:
            The current guess.
        """
        return self.__current_guess

    def get_guess_list(self):
        """
        Get the guess list.

        Returns:
            list: The guess list.
        """
        return self.__guess_list

    def fill_board(self):
        """
        Fills the board with random uppercase letters.

        Parameters:
            None

        Returns:
            None
        """
        random.seed(self.__seed)
        for i, row in enumerate(self.__board):
            for j, value in enumerate(row):
                value = random.choice(string.ascii_uppercase)
                self.__board[i][j] = f" {value} "

    # Set the seed to a specific value
    def set_seed(self):
        """
        Set the seed value for the random number generator.

        Parameters:
            None

        Returns:
            None
        """
        while True:
            try:
                num = int(input("Enter seed: "))
                while (num < 0) or (num > 9999):
                    print("Number must be within 0 and 9999.")
                    num = int(input("Enter seed: "))
                self.__seed = num
                break

            except Exception as valueError:
                print("Must be a number. ")
                continue

    # Randomize the Current Seed
    def set_seed_random(self):
        """
        Set the seed value for generating random numbers.

        This function sets the seed value for generating random numbers. The seed value is used to initialize the random number generator and ensure reproducibility. If no seed value is provided, the random number generator will be initialized with a random value.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """
        self.__seed = None

    def guess(self):
        """
        Takes user input, assigns it to the variable `s`, and stores it in the instance variable `self.__current_guess`.
        Prints the value of `self.__current_guess`.
        If the result of calling the `check_palindrome` method with the cleaned guess as an argument is `True`,
        then calls the `is_a_pal` method.
        Otherwise, calls the `not_a_pal` method.
        """
        s = str(input("Enter word (in UPPERcase) : "))
        self.__current_guess = s
        self.__guess_list.clear()
        for ch in self.clean_guess():
            self.__guess_list.append(f" {ch} ")

    def clean_guess(self):
        """
        Clean the current guess by converting it to uppercase.

        Returns:
            str: The cleaned guess as an uppercase string.
        """
        return self.__current_guess.upper()

    def depth_searh(self, kdx=0, i=0, j=0):
        """
        Performs a depth-first search on the board to find a given string.

        Args:
            s (str): The string to search for.
            kdx (int, optional): The index of the current character in the string. Defaults to 0.
            i (int, optional): The current row index on the board. Defaults to 0.
            j (int, optional): The current column index on the board. Defaults to 0.

        Returns:
            bool: True if the string is found, False otherwise.
        """
        if i < 0 or i >= 4 or j < 0 or j >= 4:
            return False
        cell_marker = self.__board[i][j].replace(" ", "")
        if self.__board[i][j] != self.__guess_list[kdx]:
            return False
        if kdx == len(self.__guess_list) - 1:
            self.__board[i][j] = f"<{cell_marker}>"
            print("Nice Job!")
            self.validate_palindrome()
            print(self)
            self.fill_board()
            return True

        temp, self.__board[i][j] = self.__board[i][j], f"<{cell_marker}>"
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for x, y in directions:
            newI, newJ = i + x, j + y
            if self.depth_searh(kdx + 1, newI, newJ):
                return True

        self.__board[i][j] = temp
        return False

    # Check every cell as the starting sequence for a depth search.
    def validate_guess(self):
        """
        Validate the given guess against the board.

        Parameters:
            s (str): The guess to be validated.

        Returns:
            bool: True if the guess is valid, False otherwise.
        """
        for i in range(len(self.__board)):
            for j in range(4):
                if self.depth_searh(0, i, j):
                    return True
        return False

    def guess_teller(self):
        """
        A function that checks if the current guess is valid and prints a corresponding message.

        Parameters:
            self (object): An instance of the class.

        Returns:
            None
        """
        if not self.validate_guess():
            print(self)
            print("Are we looking at the same board!")
            self.validate_palindrome()

    def validate_palindrome(self):
        """
        Validate the input as a palindrome and perform actions based on the result.
        """
        if self.check_palindrome(self.clean_guess()):
            self.is_a_pal()
        else:
            self.not_a_pal()

    def not_a_pal(self):
        """
        Print a message indicating that the word stored in the `__current_guess` attribute is not a palindrome.

        Parameters:
        - self: The instance of the class.

        Return:
        - None
        """
        print(f"The word {self.clean_guess()} is not a palindrome.")

    def is_a_pal(self):
        """
        Prints a message stating whether the word stored in the `__current_guess` attribute is a palindrome.
        """
        print(f"The word {self.clean_guess()} is a palindrome.")

    def check_palindrome(self, s):
        """
        Recursive function to check if a given string is a palindrome.

        Parameters:
            self (object): The instance of the class.
            s (str): The string to be checked.

        Returns:
            bool: True if the string is a palindrome, False otherwise.
        """
        i = 0
        j = len(s) - 1
        if i > j:
            return True
        if s[i] != s[j]:
            return False
        else:
            s = s[i + 1 : j]
            return self.check_palindrome(s)

    def greetings(self):
        return """
        Welcome to a simple 4 x 4 boggle game.
 
            1. Enter in a seed. If you want a random seed,
            just hit the enter button.
            2. Enter an UPPERcase word to guess.
            3. Continue the game loop or stop with yes or no.
        """

    # Test conditions
    def test_set_seed(self):
        """
        A function to test the set_seed method.

        This function calls the greetings, set_seed, and fill_board methods in order to test the set_seed method of the class.

        Parameters:
        - self: The instance of the class.

        Returns:
        - None
        """
        self.greetings()
        self.set_seed()
        self.fill_board()

    def test_case_one(self):
        """
        Executes the first test case.

        This function calls the following methods in order:
            - `greetings()`: Displays a greeting message.
            - `set_seed()`: Sets the seed for generating random numbers.
            - `fill_board()`: Fills the game board with numbers.
            - `guess()`: Prompts the user to make a guess.

        This function does not have any parameters.

        This function does not return any values.
        """
        self.greetings()
        self.set_seed()
        self.fill_board()
        print(self)
        self.guess()
        self.guess_teller()
