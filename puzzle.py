import sqlite3
import random
import numpy as np


class Puzzle:
    grid: list

    def __init__(self, grid):
        self.grid = grid

    def get_grid(self):
        """
        gathers the current shape of the grid

        :return: numpy chararray (the grid used for putting the crossword in )
        """
        return self.grid

    def set_grid(self, grid):
        """
        Updates the grid to the given grid

        :param grid: numpy chararray (the grid used for putting the crosswords in)
        """
        self.grid = grid

    def get_singleword(self, length, condition):
        """
        collects a word from the "woordenboek.db" sqlite database

        :param length: int (determines the length of the word)
        :param condition: string (extra rules for the sql query optional)
        :return: string (the word we want to fill in the grid)
        """
        con = sqlite3.connect("woordenboek.db")  # connect to data base
        c = con.cursor()  # set the cursor

        # fetch a word from the database with a given length and optional letter positions
        c.execute(f"SELECT * FROM woorden WHERE LENGTH(woord) == {length + 1} {condition} ORDER BY RANDOM() Limit 1;")

        return (c.fetchone()[0]).split("\n")[0]  # ensure the "\n" character is removed from the string

    def set_blank_grid(self, grid_size):
        """
        Sets the grid as a blank so words can be filled in

        :param grid_size: integer (determines the side lengths of the grid)
        """
        grid = np.chararray((grid_size, grid_size), 1, True)  # create a 2 dimensional chararray with specified
        # dimension sizes

        grid.fill("*")  # fill every index in the generated grid with "*" for easier readability and use

        self.set_grid(grid)  # set the grid as the newly generated grid

    def fill_grid(self, word, coordinates):
        """
        Puts a word on the coordinates in the grid

        :param word: string
        :param coordinates: list (a list of points that determines the position of the word's letters)
        """
        newgrid = self.get_grid()  # fetch the current grid

        for i in range(len(word)):  # loops trough all the indexes of the word
            c_pos = coordinates[i]  # fetch the current index's coordinates
            newgrid[(c_pos[0])][(c_pos[1])] = word[i]  # put the current letter on the fetched coordinates in the grid

        self.set_grid(newgrid)  # update the grid with the newly filled in word

    def get_intersection_info(self, coordinates):
        """
        Checks if the coordinate points cross with a letter or not

        :param coordinates: lst (the coordinates the word wants to follow)
        :return: lst (info about where the word will cross with a letter)
        """
        grid = self.get_grid()  # fetch the current grid
        intersections = []  # make an empty list that will store the character's of each point

        for c in coordinates:  # loop through all the coordinate points
            # fetch and append the character on the grid with the coordinates of the current point
            intersections.append(grid[c[0]][c[1]])

        return intersections

    def generate_coordinate(self, word_length, axis, grid_size):
        """
        generates pseudo random coordinates for a word

        :param word_length: interger (determines the lenght of the coordinates and word)
        :param axis: list (determines if the word is vertical or horizontal)
        :param grid_size: integer
        :return: list (list with the coordiantes for the word)
        """
        grid = self.get_grid()  # fetch the current grid
        coordinates = []  # create a list that will contain our generated coordinates
        tmp = []  # create a list that will contain a sub grid of the original

        # create a grid with the original grid dimensions minus the length of the word
        for i in range(grid_size - word_length):
            tmp.append(grid[i])  # create the sub grid

        index_rows = np.shape(tmp)[0] - 1  # gather the indexes of the sub-grid's rows
        index_column = np.shape(tmp)[1] - 1  # gather the indexes of the sub-grid's column's

        # check is the axis of the coordinates is horizontal or vertical
        if axis == [0, 1]:
            # start on a point where the word can move horizontal and not go outside the original grid
            start = [random.randint(0, index_column), random.randint(0, index_rows)]
        else:
            # start on a point where the word can move vertically and not go outside the original grid
            start = [random.randint(0, index_rows), random.randint(0, index_column)]

        coordinates.append(start)  # store the coordinate in the coordinate list

        # loop trough the rest of the points on the given axis
        for i in range(word_length - 1):
            start = start[0] + axis[0], start[1] + axis[1]  # determine the next point
            coordinates.append(start)  # store the coordinate in the coordinate list

        return coordinates

    def get_crossword(self, min_length, max_length, grid_size, used_coordinates, words, min_crossings, max_crossings,
                      axis, currently_faulty_coordinates, repeats):
        """
        determines if a word can be put on the grid with the given coordinates, creates a condition for the SQL query
        and initiates the filling of the grid for a single word

        :param min_length: integer (determines the minimal lenght of the word)
        :param max_length: integer (determines the max lenght of the word)
        :param grid_size: integer (dimension sizes of the grid)
        :param used_coordinates: list (coordinates that are already in use on the axis)
        :param words: list (a list of words that are used in te grid, this list wil be used in the gui)
        :param min_crossings: integer (the minimal amount of crossings between words)
        :param max_crossings: integer (the maximal amount of crossings between words)
        :param axis: list (determines the axis of the word)
        :param currently_faulty_coordinates: list (a list with coordinates that are faulty in the current iteration)
        :param repeats: integer (the amount of times the has called itself)
        :return: list, list (the coordinates that are now in use on the axis and a list of the words on the grid)
        """
        # if the functions has called itself more than 50 times return an error so a entirely new grid will be generated
        # this is done to prevent a stack overflow if the grid starts with a word that is hard to cross with
        if repeats > 50:
            return TypeError
        else:
            word_lenght = random.randint(min_length, max_length)  # generate a random word length

            # create a list where the individual coordinate points will be stored in so they can be compared easier
            used_point_lst = []

            # puts the individual coordinate points in the corresponding list
            for used_coordinate_set in used_coordinates:
                for used_point in used_coordinate_set:
                    used_point_lst.append(used_point)

            # generate coordinates for the generated word length
            gen_coordinates = self.generate_coordinate(word_lenght, axis, grid_size)

            # gather info about the generated coordinates
            intersection_info = self.get_intersection_info(gen_coordinates)

            # check if the generated coordinates have valid crossings
            for point in gen_coordinates:  # loop true all the individual generated points
                # checks if the points are already in use and if the amount of crossings is invalid
                if point in used_point_lst or \
                        gen_coordinates in currently_faulty_coordinates \
                        or intersection_info.count("*") >= word_lenght + 1 - min_crossings \
                        or intersection_info.count("*") < word_lenght - max_crossings:
                    # store the generated coordinates for this iteration as invalid
                    currently_faulty_coordinates.append(gen_coordinates)

                    repeats += 1

                    # retry generating filling in a word with the updated information and a different word length
                    return self.get_crossword(min_length, max_length, grid_size, used_coordinates, words, min_crossings,
                                              max_crossings, axis, currently_faulty_coordinates, repeats)

            # generate a condition so a valid word can be filled in the grid
            if intersection_info.count("*") == word_lenght:  # if the word doesnt cross make the condition empty
                condition = ""
            else:  # create condition
                condition = "AND woord LIKE '"  # create the start of the condition
                # loop trough all the points where word is being positioned
                for i in intersection_info:
                    if i == "*":  # if the point is doesnt cross with a letter ad a "_" to the condition
                        condition = (condition + "_")
                    else:  # if the point crosses with a letter add the letter to the condition
                        condition = (condition + f"{i}")

                condition = (condition + "%'")  # add "%'" to the condition so the correct word will be fetched

            # tries to fetch the word with the condition
            try:
                word = self.get_singleword(word_lenght, condition)  # fetch a word with the build condition
                words.append(word)  # store the word in a list with all the used words on this axis
                # store the coordinates in a list with all the used coordinates on this axis
                used_coordinates.append(gen_coordinates)

                self.fill_grid(word, gen_coordinates)  # fill the grid with the word on the generated coordinates
            except TypeError:  # if a word with the conditions cant be fetched retry generating filling in a word

                # store the generated coordinates for this iteration as invalid
                currently_faulty_coordinates.append(gen_coordinates)

                repeats += 1

                return self.get_crossword(min_length, max_length, grid_size, used_coordinates, words, min_crossings,
                                          max_crossings, axis, currently_faulty_coordinates, repeats)

            return used_coordinates, words

    def fill_in_crosswords(self, word_count, min_length, max_length, min_crossings, max_crossings, grid_size):
        """
        initiates the filling of the grid

        :param word_count: int (determines the amount of words in the puzzle)
        :param min_length: integer (determines the minimal length of the word)
        :param max_length: integer (determines the max length of the word)
        :param min_crossings: integer (the minimal amount of crossings between words)
        :param max_crossings: integer (the maximal amount of crossings between words)
        :param grid_size: integer (dimension sizes of the grid)
        :return: list, list, list, list (list with horizontal/vertical words, and coordinates)
        """
        h_words = []  # create a list where all the horizontal words will be stored
        v_words = []  # create a list where all the vertical words will be stored

        h_coordinates = []  # create a list where all the horizontal coordinates will be stored
        v_coordinates = []  # create a list where all the vertical coordinates will be stored

        try:
            # generate initial vertical and horizontal words with less than minimal crossings so the rest of the
            # words can be generated normally

            initial_min_crossings = 0
            for i in range(min_crossings):  # generate initial words for the amount of minimal crossings
                h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates, h_words,
                                                            initial_min_crossings, max_crossings, [0, 1], [], 0)
                initial_min_crossings += 1

                v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates, v_words,
                                                            initial_min_crossings, max_crossings, [1, 0], [], 0)

            # generate the left over words that need to be generated
            for i in range(int(word_count - (word_count / 2) - min_crossings)):
                h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates, h_words,
                                                            min_crossings, max_crossings, [0, 1], [], 0)

                v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates, v_words,
                                                            min_crossings, max_crossings, [1, 0], [], 0)

            return h_coordinates, v_coordinates, h_words, v_words

        except TypeError:
            # retry the entire process of filling the grid if
            # during filling the grid a function results in a value error
            self.set_blank_grid(grid_size)  # set the grid as a blank
            return self.fill_in_crosswords(word_count, min_length, max_length, min_crossings, max_crossings, grid_size)

    def generate_puzzle(self, word_count, min_length, max_length, min_crossings, max_crossings):
        """
        initiates the entire process of generating a crossword puzzle

        :param word_count: int (determines the amount of words in the puzzle)
        :param min_length: integer (determines the minimal length of the word)
        :param max_length: integer (determines the max length of the word)
        :param min_crossings: integer (the minimal amount of crossings between words)
        :param max_crossings: integer (the maximal amount of crossings between words)
        :return:
        """
        # calculate the size of the grid
        if word_count > max_length:
            grid_size = word_count + 2
        else:
            grid_size = max_length + 2

        self.set_blank_grid(grid_size)  # set the grid so it can be used

        h_coordinates, v_coordinates, h_words, v_words = self.fill_in_crosswords(word_count, min_length, max_length,
                                                                                 min_crossings, max_crossings,
                                                                                 grid_size)

        return self.get_grid(), h_coordinates, v_coordinates, h_words, v_words, grid_size
