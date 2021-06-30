import sqlite3
import random
import numpy as np
import string


class Puzzle:
    grid: list
    unusable_cells: list

    def __init__(self, grid, unusable_cells):
        self.grid = grid
        self.unusable_cells = unusable_cells

    def get_unusable_cells(self):
        """
        gathers the current list of unusable cells

        :return: numpy chararray (the grid used for putting the crossword in )
        """
        return self.unusable_cells

    def set_unusable_cells(self, unusable_cells):
        """
        Updates the unusable_cells lst

        :param unusable_cells: list (contains all the cells where a crossword cell cant be placed anymore)
        """
        self.unusable_cells = unusable_cells

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

        :param word_length: integer (determines the length of the coordinates and word)
        :param axis: list (determines if the word is vertical or horizontal)
        :param grid_size: integer
        :return: list (list with the coordinates for the word)
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
            start = [start[0] + axis[0], start[1] + axis[1]]  # determine the next point
            coordinates.append(start)  # store the coordinate in the coordinate list

        return coordinates

    def get_cel_borders(self, axis, used_coordinates, used_opposite_coordinates):
        """
        defines the borders of all the cells that are in use

        :param axis: list (determines if the word is vertical or horizontal)
        :param used_coordinates: used_coordinates: list (coordinates that are already in use on the axis)
        :param used_opposite_coordinates: list (used coordinates on the other axis than the word that is generated)
        :return:
        """
        # create a list where the individual coordinate points will be stored in so they can be compared easier
        used_point_lst = []
        used_point_lst_left = []
        used_point_lst_right = []
        right_used_opposite_points_lst = []
        left_used_opposite_points_lst = []

        # puts the individual coordinate points in the corresponding list of the current axis
        for used_coordinate_set in used_coordinates:
            for used_point in used_coordinate_set:
                # if the point is bigger than zero define the left and right side, else only the right side
                if used_point[0] > 0 or used_point[1] > 0:
                    used_point_lst.append(used_point)

                    used_point_lst_right.append([used_point[0] + axis[1], used_point[1] + axis[0]])
                    used_point_lst_left.append([used_point[0] - axis[1], used_point[1] - axis[0]])
                else:
                    used_point_lst.append(used_point)

                    used_point_lst_right.append([used_point[0] + axis[1], used_point[1] + axis[0]])

        # puts the individual coordinate points in the corresponding list of the opposite axis
        for used_coordinate_set in used_opposite_coordinates:
            for used_point in used_coordinate_set:
                # if the point is bigger than zero define the left and right side, else only the right side
                if used_point[0] >= 0 or used_point[1] >= 0:

                    right_used_opposite_points_lst.append([used_point[0] + axis[0], used_point[1] + axis[1]])
                    left_used_opposite_points_lst.append([used_point[0] - axis[0], used_point[1] - axis[1]])
                else:
                    right_used_opposite_points_lst.append([used_point[0] + axis[0], used_point[1] + axis[1]])

        return used_point_lst, used_point_lst_left, used_point_lst_right, \
               right_used_opposite_points_lst, left_used_opposite_points_lst

    def get_crossword(self, min_length, max_length, grid_size, used_coordinates, used_opposite_coordinates, words,
                      min_crossings, max_crossings,
                      axis, currently_faulty_coordinates, repeats):
        """
        determines if a word can be put on the grid with the given coordinates, creates a condition for the SQL query
        and initiates the filling of the grid for a single word

        :param used_opposite_coordinates: list (used coordinates on the other axis than the word that is generated)
        :param min_length: integer (determines the minimal length of the word)
        :param max_length: integer (determines the max length of the word)
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
        if repeats > 60:
            return TypeError
        else:
            word_length = random.randint(min_length, max_length)  # generate a random word length

            used_point_lst, used_point_lst_left, used_point_lst_right, \
                right_used_opposite_coordinates, \
                left_used_opposite_points_lst = self.get_cel_borders(axis, used_coordinates, used_opposite_coordinates)

            # generate coordinates for the generated word length
            gen_coordinates = self.generate_coordinate(word_length, axis, grid_size)

            # gather info about the generated coordinates
            intersection_info = self.get_intersection_info(gen_coordinates)
            unusable_cells = self.get_unusable_cells()
            # check if the generated coordinates have valid crossings
            for point in gen_coordinates:  # loop true all the individual generated points
                # checks if the points are already in use or if the amount of crossings is invalid or
                # if the generated coordinates intersect with certain borders it can not intersect with
                point = [point[0], point[1]]
                if point in used_point_lst or \
                        point in used_point_lst_right or \
                        point in used_point_lst_left or \
                        point in unusable_cells or \
                        gen_coordinates[0] in right_used_opposite_coordinates or \
                        gen_coordinates[len(gen_coordinates) - 1] in left_used_opposite_points_lst or \
                        gen_coordinates in currently_faulty_coordinates \
                        or intersection_info.count("*") >= word_length + 1 - min_crossings \
                        or intersection_info.count("*") < word_length - max_crossings:
                    # store the generated coordinates for this iteration as invalid
                    currently_faulty_coordinates.append(gen_coordinates)

                    repeats += 1

                    # retry generating filling in a word with the updated information and a different word length
                    return self.get_crossword(min_length, max_length, grid_size, used_coordinates,
                                              used_opposite_coordinates, words, min_crossings, max_crossings, axis,
                                              currently_faulty_coordinates, repeats)

            # generate a condition so a valid word can be filled in the grid
            if intersection_info.count("*") == word_length:  # if the word doesnt cross make the condition empty
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
                word = self.get_singleword(word_length, condition)  # fetch a word with the build condition

                words.append(word)  # store the word in a list with all the used words on this axis

                # store the coordinates in a list with all the used coordinates on this axis
                used_coordinates.append(gen_coordinates)

                if gen_coordinates[0][0] >= 0 or gen_coordinates[0][1] >= 0:
                    unusable_cells.append([gen_coordinates[0][0] - axis[0], gen_coordinates[0][1] - axis[1]])

                unusable_cells.append([gen_coordinates[(len(gen_coordinates) - 1)][0] + axis[0],
                                       gen_coordinates[(len(gen_coordinates) - 1)][1] + axis[1]])

                self.set_unusable_cells(unusable_cells)

                self.fill_grid(word, gen_coordinates)  # fill the grid with the word on the generated coordinates
                return used_coordinates, words

            except TypeError:  # if a word with the conditions cant be fetched retry generating filling in a word
                # store the generated coordinates for this iteration as invalid
                currently_faulty_coordinates.append(gen_coordinates)

                repeats += 1

                return self.get_crossword(min_length, max_length, grid_size, used_coordinates,
                                          used_opposite_coordinates, words, min_crossings, max_crossings, axis,
                                          currently_faulty_coordinates, repeats)

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

        val = word_count

        try:
            val -= min_crossings * 2
            h_amount = int(val - random.randint(round(val / 3), round(val / 2)))
            v_amount = int(val - h_amount)
            # generate initial vertical and horizontal words with less than minimal crossings so the rest of the
            # words can be generated normally

            initial_min_crossings = 0
            for i in range(min_crossings):  # generate initial words for the amount of minimal crossings

                h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates,
                                                            v_coordinates, h_words, initial_min_crossings,
                                                            max_crossings, [0, 1], [], 0)
                initial_min_crossings += 1
                v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates,
                                                            h_coordinates, v_words, initial_min_crossings,
                                                            max_crossings, [1, 0], [], 0)
            # generate the left over words that need to be generated
            for i in range(h_amount + v_amount):
                if v_amount <= 0 and h_amount <= 0:
                    break
                else:
                    if h_amount > 0:
                        h_amount -= 1
                        h_coordinates, h_words = self.get_crossword(min_length, max_length, grid_size, h_coordinates,
                                                                    v_coordinates, h_words,
                                                                    min_crossings, max_crossings, [0, 1], [], 0)
                    if v_amount > 0:
                        v_amount -= 1
                        v_coordinates, v_words = self.get_crossword(min_length, max_length, grid_size, v_coordinates,
                                                                    h_coordinates, v_words,
                                                                    min_crossings, max_crossings, [1, 0], [], 0)
            return h_coordinates, v_coordinates, h_words, v_words

        except TypeError:
            # retry the entire process of filling the grid if
            # during filling the grid a function results in a value error
            self.set_blank_grid(grid_size)  # set the grid as a blank
            self.set_unusable_cells([])  # reset the unusable cells
            return self.fill_in_crosswords(word_count, min_length, max_length, min_crossings, max_crossings, grid_size)

    def generate_puzzle(self, word_count, min_length, max_length, min_crossings, max_crossings, option):
        """
        initiates the entire process of generating a crossword puzzle or a find the word puzzle

        :param option: integer (1 or a 0 determines if what kind of puzzle the code is)
        :param word_count: int (determines the amount of words in the puzzle)
        :param min_length: integer (determines the minimal length of the word)
        :param max_length: integer (determines the max length of the word)
        :param min_crossings: integer (the minimal amount of crossings between words)
        :param max_crossings: integer (the maximal amount of crossings between words)
        :return:
        """
        grid_size = 18

        self.set_blank_grid(grid_size)  # set the grid so it can be used

        h_coordinates, v_coordinates, h_words, v_words = self.fill_in_crosswords(word_count, min_length, max_length,
                                                                                 min_crossings, max_crossings,
                                                                                 grid_size)
        grid = self.get_grid()

        # put a random lowercase letter on empty points in the grid
        if option == 0:
            for y in range(grid_size):
                for x in range(grid_size):
                    if grid[y][x] == "*":
                        grid[y][x] = random.choice(string.ascii_lowercase)

        return self.get_grid(), h_coordinates, v_coordinates, h_words, v_words, grid_size
