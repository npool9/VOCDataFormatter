import os
from random import shuffle
import datetime


class DataSplitter:
    """
    This class is tasked with splitting all of our data into positive vs. negative examples as well as splitting into
    training, validation, and test data.
    ASSUMPTIONS:
        1. We already have the VOCdevkit downloaded
        2. The image dataset we're working with is organized such that each class is in its own directory
    """

    def __init__(self, dataset_path, classes):
        """
        Initialize the DataSplitter.
        :param dataset_path: the path the user has given to the root directory of his/her dataset
        :param classes: the list of images classes that the user is wishing to classify
        """
        self.training_ids = []
        self.validation_ids = []
        self.testing_ids = []
        self.dataset_path = dataset_path
        self.classes = classes
        self.year = str(datetime.datetime.now().year)
        self.isSplit = input("Is your data already split into training/validation/test sets? y/n")

    def split(self):
        """
        Split the data into training, validation, and test sets. The ids of each image are saved into the DataSplitter
        class's respective lists (i.e. training_ids, validation_ids, testing_ids).
        """
        if self.isSplit[0].lower() == 'y':
            # TODO: Handle pre-defined lists of training/validation/test sets by id e.g. ['2019_000001', ...]
            print("Handling existing training/validation/test split specifications is not a feature at this time.")
            print("Exiting...")
            exit(0)
        else:
            train_percent = 0.5
            valid_percent = 0.1
            # test_percent = 0.4
            for c in self.classes:
                c_path = self.dataset_path + '/' + c
                images = os.listdir(c_path)
                # get rid of irrelevant, hidden files from the image list
                for image in images:
                    if image[0] == '.':
                        images.remove(image)
                num_images = len(images)
                num_train = int(num_images * train_percent)
                num_valid = int(num_images * valid_percent)
                num_test = num_images - num_train - num_valid  # test set gets the remaining number of images
                # Randomly permute the image set so that there is no notion of order
                images = shuffle(images)
                for i in range(num_train):
                    self.training_ids.append(images[i][:images[i].index('.')])  # don't include file extension
                for i in range(num_train, num_train + num_valid):
                    self.validation_ids.append(images[i][:images[i].index('.')])
                for i in range(num_train + num_valid, num_train + num_valid + num_test):
                    self.test_ids.append(images[i][:images[i].index('.')])
        self.save_to_files()

    def save_to_files(self):
        """
        Save the data split specifications to text files for each class in VOC PASCAL format.
        There will be r files: train.txt, val.txt, trainval.txt, test.txt
        There will also be 4 additional files per class: <class_name>_train.txt, <class_name>_val.txt,
            <class_name>_trainval.txt, <class_name>_test.txt
        """
        object_dict = self.get_object_ids()
        kit_path = input('Enter the path your VOCdevkit directory:\n')
        if kit_path.endswith('/'):
            kit_path = kit_path[:-1]
        specs_path = kit_path + '/VOC' + self.year + '/ImageSets/Main/'
        train_file = open(specs_path + 'train.txt', 'w')
        val_file = open(specs_path + 'val.txt', 'w')
        trainval_file = open(specs_path + 'trainval.txt', 'w')
        test_file = open(specs_path + 'test.txt', 'w')
        is_first_line = 1
        for image_id in self.training_ids:
            if is_first_line:
                train_file.write(image_id)
                trainval_file.write(image_id)
            else:
                train_file.write('\n' + image_id)
                trainval_file.write('\n' + image_id)
            is_first_line = 0
        is_first_line = 1
        for image_id in self.validation_ids:
            if is_first_line:
                val_file.write(image_id)
            else:
                val_file.write('\n' + image_id)
            # assuming that at least one training example image id has been written to trainval.txt already
            # as it should be!
            trainval_file.write('\n' + image_id)
            is_first_line = 0
        is_first_line = 1
        for image_id in self.testing_ids:
            if is_first_line:
                test_file.write(image_id)
            else:
                test_file.write('\n' + image_id)
            is_first_line = 0

        # Create 4 text files per class with ids in left column and 1 for positive example and -1 for negative
        #  in right column
        for c in self.classes:
            train_file = open(specs_path + c + '_train.txt', 'w')
            val_file = open(specs_path + c + '_val.txt', 'w')
            trainval_file = open(specs_path + c + '_trainval.txt', 'w')
            test_file = open(specs_path + c + '_test.txt', 'w')
            c_cap = c.capitalize()
            is_first_line = 1
            for image_id in self.training_ids:
                if (image_id in os.listdir(self.dataset_path + '/' + c)
                        or image_id in os.listdir(self.dataset_path + '/' + c_cap)):
                    if is_first_line:
                        train_file.write(image_id + ' 1')
                        trainval_file.write(image_id + ' 1')
                    else:
                        train_file.write('\n' + image_id + ' 1')
                        trainval_file.write('\n' + image_id + ' 1')
                else:
                    if is_first_line:
                        train_file.write(image_id + ' -1')
                        trainval_file.write(image_id + ' -1')
                    else:
                        train_file.write('\n' + image_id + ' -1')
                        trainval_file.write('\n' + image_id + ' -1')
                is_first_line = 0
            is_first_line = 1
            for image_id in self.validation_ids:
                if (image_id in os.listdir(self.dataset_path + '/' + c)
                        or image_id in os.listdir(self.dataset_path + '/' + c_cap)):
                    if is_first_line:
                        val_file.write(image_id + ' 1')
                        trainval_file.write(image_id + ' 1')
                    else:
                        val_file.write('\n' + image_id + ' 1')
                        trainval_file.write('\n' + image_id + ' 1')
                else:
                    if is_first_line:
                        val_file.write(image_id + ' -1')
                        trainval_file.write(image_id + ' -1')
                    else:
                        val_file.write('\n' + image_id + ' -1')
                        trainval_file.write('\n' + image_id + ' -1')
                is_first_line = 0
            is_first_line = 1
            for image_id in self.testing_ids:
                if (image_id in os.listdir(self.dataset_path + '/' + c)
                        or image_id in os.listdir(self.dataset_path + '/' + c_cap)):
                    if is_first_line:
                        test_file.write(image_id + ' 1')
                    else:
                        test_file.write('\n' + image_id + ' 1')
                else:
                    if is_first_line:
                        test_file.write(image_id + ' -1')
                    else:
                        test_file.write('\n' + image_id + ' -1')
                is_first_line = 0

    def get_object_ids(self):
        """
        Get lists of ids that correspond to each class (i.e. the positive examples for each class)
        :return: a dictionary where they key is the class name and the value is the list of its corresponding image ids
        """
        object_dict = dict()
        for c in self.classes:
            image_ids = []
            image_class_path = self.dataset_path + '/' + c
            for image_id in os.listdir(image_class_path):
                image_ids.append(image_id[:image_id.index('.')])  # don't include file extension
            # key: class name
            # value: image_ids
            # add this pair to the object dictionary
            object_dict[c.lower()] = image_ids
        return object_dict
