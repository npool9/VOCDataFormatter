"""
Initializes all of the components that contribute to putting an image dataset into PASCAL VOC format. This will be
quite useful for using current implementations that were originally used for the VOC object detection competition on
your own dataset --- not the original VOC PASCAL dataset.
ASSUMPTIONS:
    1. We already have the VOCdevkit downloaded
    2. The image dataset we're working with is organized such that each class is in its own directory
"""
import data_renamer


class Main:

    """
    Initialize each component of transforming image dataset in to PASCAL VOC format.
    """
    def __init__(self):
        self.renamer = data_renamer.DataRenamer()

    """
    Run each component of the PASCAL VOC dataset formatter in sequence.
    """
    def begin(self):
        self.renamer.rename()


if __name__ == "__main__":
    main = Main()
    main.begin()