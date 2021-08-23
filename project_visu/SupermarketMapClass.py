""" 
SupermarketMap Class for drawing supermarket map.
"""


import numpy as np
import cv2
import constants


# dictionary mapping character to tile coordinate
CHAR_TO_TEIL = {
    "#":[0, 0], "G":[7, 3], "C":[2, 8], "F":[1, 14], "S":[0, 14],
    "A":[4, 9], "I":[5, 9], "R":[7, 4], "D":[7, 8], ".":[1, 2]
    }


class SupermarketMap:
    """Visualizes the supermarket background"""


    def __init__(self):
        self.tiles = constants.TILES # image containing tiles used for drawing
        # split the layout string into a two dimensional matrix
        self.contents = [list(row) for row in constants.MARKET.split("\n")]
        self.ncols = len(self.contents[0])
        self.nrows = len(self.contents)
        self.image = np.zeros(
            (self.nrows*constants.TILE_SIZE, self.ncols*constants.TILE_SIZE, 3), dtype=np.uint8
        )
        self.prepare_map()


    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = row*constants.TILE_SIZE
        x = col*constants.TILE_SIZE
        return self.tiles[y:y+constants.TILE_SIZE, x:x+constants.TILE_SIZE]


    def get_tile(self, char):
        """returns the array for a given tile character"""
        return self.extract_tile(CHAR_TO_TEIL[char][0], CHAR_TO_TEIL[char][1])


    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.contents):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = row*constants.TILE_SIZE
                x = col*constants.TILE_SIZE
                self.image[y:y+constants.TILE_SIZE, x:x+constants.TILE_SIZE] = bm


    def draw(self, frame):
        """
        draws the image into a frame
        """
        # frame is background = np.zeros((500, 700, 3), np.uint8)
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image


    def write_image(self, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, self.image)
