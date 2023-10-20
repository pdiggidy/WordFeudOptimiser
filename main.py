import numpy as np
import screenshot_processing as sp

# Read in the words from the file
with open('cleaned_words.txt', 'r') as f:
    word_list = f.read().splitlines()


class Grid():
    def __init__(self, size=15):
        self.size = size
        self.grid = np.zeros((size, size))

    def set_grid(self, grid):
        self.grid = grid

    def get_grid(self):
        return self.grid


def main():
    grid = Grid()
    print(grid.get_grid())
    grid, letters = sp.screenshot_processing('Test_screenshot.jpg')


if __name__ == '__main__':
    main()
