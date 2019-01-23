import os
import datetime


class DataRenamer:
    """
    This class is devoted to taking the data you have a renaming it according to VOC PASCAL naming conventions.
    ASSUMPTIONS:
        1. We already have the VOCdevkit downloaded
        2. The image dataset we're working with is organized such that each class is in its own directory
    """

    def __init__(self):
        """
        Initialize the class. dataset_path will be provided by the user, and it is the root directory of the dataset.
        This root directory only contains subdirectories such that each one of those is contains every image of its
        corresponding class. E.g. subdirectories named 'Person', 'Car', etc.
        """
        self.dataset_path = input("Enter the root directory of the dataset:\n")
        self.year = str(datetime.datetime.now().year)

    def rename(self):
        """
        Rename each image in the dataset given each class of images in the dataset_path.
        :return: the path to the root directory and a list of the image classes
        """
        dirs = self.get_classes()
        num_dirs = len(dirs)
        last_file_num = 0
        for i in range(num_dirs):
            print("Subdirectory Name:", dirs[i])
            path = self.dataset_path + '/' + dirs[i]
            images = os.listdir(path)
            for image in images:
                if image[0] == '.':
                    images.remove(image)
            num_images = len(images)
            for j in range(num_images):
                ext = images[j][images[j].index('.'):]
                id_num = str(last_file_num + j + 1)
                # append 0's to id_num based on its length without them. There should be 6 digits in the ID number
                # not counting the year at the beginning.
                zeros = ''.join(['0' for i in range(6 - len(str(id_num)))])
                new_file_name = self.year + '_' + zeros + id_num
                print(new_file_name)
                os.rename(path + '/' + images[j], path + '/' + new_file_name + ext)
            last_file_num += j + 1
        return self.dataset_path, dirs

    def get_classes(self):
        """
        Get a list of the image classes. These, by assumption, correspond to the subdirectories in the root directory
        passed by the user to the program.
        :return: a list of strings corresponding to the images classes in the user's dataset
        """
        dirs = os.listdir(self.dataset_path)
        # get rid of hidden files in the list of directories
        for directory in dirs:
            if directory[0] == '.':
                dirs.remove(directory)
        return dirs
