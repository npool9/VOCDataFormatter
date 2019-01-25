import data_renamer
import data_splitter
import annotation_maker


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
        self.kit_path = None
        self.annotation_maker = None

    def begin(self):
        """
        Run each component of the PASCAL VOC dataset formatter in sequence.
        """
        dataset_path, classes = self.renamer.rename()
        self.data_splitter = data_splitter.DataSplitter(dataset_path, classes)
        self.data_splitter.split()
        self.annotation_maker = annotation_maker.AnnotationMaker(dataset_path, self.kit_path)

    def set_kit_path(self, kit_path):
        """
        Simply retrieve the path of the VOCdevkit from the user. This function is called by DataSplitter
        :param kit_path: a string of the path to the VOCdevkit directory
        """
        self.kit_path = kit_path


if __name__ == "__main__":
    main = Main()
    main.begin()
