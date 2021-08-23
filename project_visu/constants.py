"""
Constants used in both SupermarketMapClass and CustomerClass.
"""

import cv2

TILES = cv2.imread("tiles.png")

TILE_SIZE = 32

# states from left to right : drinks, diary, spices, fruits
# checkout left, entrance right
MARKET = """
##################
##..............##
##..DR..IA..SF..##
##..DR..IA..SF..##
##..DR..IA..SF..##
##..DR..IA..SF..##
##..DR..IA..SF..##
##..............##
##..C#..C#..C#..##
##..##..##..##..##
##..............##
##GG##########GG##
""".strip()
