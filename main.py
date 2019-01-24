import data_renamer
import data_splitter


class Main:
    """
    Initializes all of the components that contribute to putting an image dataset into PASCAL VOC format. This will be
    quite useful for using current implementations that were originally used for the VOC object detection competition on
    your own dataset --- not the original VOC PASCAL dataset.
    ASSUMPTIONS:
        1. We already have the VOCdevkit downloaded
        2. The image dataset we're working with is organized such that each class is in its own directory
    """

    def __init__(self):
        """
        Initialize each component of transforming image dataset in to PASCAL VOC format.
        """
        self.renamer = data_renamer.DataRenamer()
        self.data_splitter = None

    def begin(self):
        """
        Run each component of the PASCAL VOC dataset formatter in sequence.
        """
        dataset_path, classes = self.renamer.rename()
        self.data_splitter = data_splitter.DataSplitter(dataset_path, classes)
        self.data_splitter.split()


if __name__ == "__main__":
    main = Main()
    main.begin()
