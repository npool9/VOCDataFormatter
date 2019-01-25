import data_renamer
import data_splitter
import annotation_maker
import datetime
import os


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
        self.dataset_path = input('Enter the path to the root directory of your dataset:\n')
        self.classes = [c.lower() for c in os.listdir(self.dataset_path)]
        self.year = str(datetime.datetime.now().year)
        self.kit_path = input("Enter the path ot your VOCdevkit directory:\n")
        self.annotation_path = self.kit_path + '/VOC' + self.year + '/Annotations'
        self.renamer = data_renamer.DataRenamer(self.dataset_path, self.year)
        self.data_splitter = data_splitter.DataSplitter(self.dataset_path, self.classes, self.year, self.kit_path)
        self.annotation_maker = annotation_maker.AnnotationMaker(self.dataset_path, self.kit_path, self.year,
                                                                 self.annotation_path)

    def begin(self):
        """
        Run each component of the PASCAL VOC dataset formatter in sequence.
        """

        self.renamer.rename()
        self.data_splitter.split()
        self.annotation_maker.build()

    def set_kit_path(self, kit_path):
        """
        Simply retrieve the path of the VOCdevkit from the user. This function is called by DataSplitter
        :param kit_path: a string of the path to the VOCdevkit directory
        """
        self.kit_path = kit_path


if __name__ == "__main__":
    main = Main()
    main.begin()
