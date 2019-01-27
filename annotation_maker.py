import os
import numpy as np
from matplotlib.image import imread


class AnnotationMaker:
    """
    This class is tasked with creating appropriate XML annotations for object detection of each image in the provided
    dataset. Each annotation will be in the proper VOC PASCAL format and saved in the directory for VOC helper
    functions to find.
    ASSUMPTIONS:
        1. We already have the VOCdevkit downloaded
        2. The image dataset we're working with is organized such that each class is in its own directory
    """

    def __init__(self, dataset_path, dev_kit_path, year, annotation_path):
        """
        Initialize the VOC xml annotation-maker
        :param dataset_path: the path of the image dataset
        :param dev_kit_path: the path of VOCdevkit
        :param year: the current year and the year that will go in this file naming convention: VOC<year>
        :param annotation_path: the path in the VOCdevkit directory where VOC convention expects annotations to exist
        """
        self.dataset_path = dataset_path
        self.dev_kit_path = dev_kit_path
        self.year = year
        self.annotation_path = annotation_path

    def xml_writer(self, filename, object_class, box, num_objects=1, difficult='0', occluded='0', pose='Unspecified',
                   truncated='0', segmented='0', database='Unknown', im='Unknown'):
        """
        The writer of the tags that populate each annotation xml file for each image.
        :param filename: the filename of the image (including its extension)
        :param object_class: the image/object's class (also the subdirectory name based on the script's assumptions)
        :param box: the bounding box of the objects in the image i.e. [[xmax, xmin, ymax, ymin], ...]
         ASSUMPTIONS:
          1. There is only one object per image
          2. The task is classification, and therefore the bounding box of each object is the border of the image
            NOTE: if you have other bounding box information, provide each bounding box as a row of a numpy array
        :param num_objects: the number of objects in the image (ordered the same way as the box parameter)
        :param difficult: either 1 or 0
        :param occluded: either 1 or 0
        :param pose: not familiar with this parameter
        :param truncated: not familiar with this parameter
        :param segmented: assumption is that the task is classification/detection
        :param database: the source of the image/object data
        :param im: any other notes about the input image
        :return: the contents of the xml annotation file for a single image
        """
        image = imread(self.dataset_path + '/' + object_class + '/' + filename)
        object_tags = ""
        for i in range(num_objects):
            object_tags += ('\n\t<object>' + '\n\t\t<name>' + object_class.lower() +
                  '</name>\n\t\t<bndbox>\n\t\t\t<xmax>' + box[i][0] + '</xmax>\n'
                  + '\t\t\t<xmin>' + box[i][1] + '</xmin>\n\t\t\t<ymax>' + box[i][2] + '</ymax>\n\t\t\t' + '<ymin>' +
                  box[i][3] + '</ymin>\n\t\t</bndbox>\n\t\t<difficult>' + difficult + '</difficult>\n\t\t<occluded>' +
                  occluded + '</occluded>\n\t\t<pose>' + pose + '</pose>\n\t\t<truncated>' + truncated +
                  '</truncated>\n\t</object>')
        xml = ('<annotation>\n\t<filename>' + filename + '</filename>\n\t<folder>VOC' + self.year +
                  '</folder>' + object_tags + '\n\t<size>\n\t\t<depth>' + str(image.shape[2]) + '</depth>\n\t\t<height>'
                  + str(image.shape[1]) + '</height>' + '\n\t\t<width>' + str(image.shape[0]) +
                  '</width>\n\t</size>\n\t<segmented>' + segmented + '</segmented>' + '\n\t<source>\n\t\t' +
                  '<annotation>Nathan Pool</annotation>\n\t\t<database>' + database + '</database>'
                  + '\n\t\t<image>' + im + '</image>\n\t</source>\n</annotation>')
        return xml

    def build(self):
        """
        The loop that controls the building of every xml annotation file for every image in the dataset.
        """
        classes = os.listdir(self.dataset_path)
        for c in classes:
            if self.dataset_path.endswith('/'):
                self.dataset_path = self.dataset_path[:-1]
            if os.path.isdir(self.dataset_path + '/' + c):
                im_files = os.listdir(self.dataset_path + '/' + c)  # note we lowered the case of subdirectory names
                for im_file in im_files:
                    if im_file[0] == '.':
                        im_files.remove(im_file)  # remove hidden files from the list. They are not images.
                for im_file in im_files:
                    image = imread(self.dataset_path + '/' + c + '/' + im_file)
                    # note our default bounding box implies classification vs detection (the border of the image)
                    #  you can provide your own list of lists structure to capture the number of objects in each
                    #  of your images
                    bbox = [[str(image.shape[0]), str(0), str(image.shape[1]), str(0)]]
                    xml = self.xml_writer(im_file, c, bbox)
                    # Now, save the file to the annotation path obeying VOC PASCAL formatting expectations
                    f = open(self.annotation_path + '/' + im_file[:im_file.index('.')] + '.xml', 'w')
                    f.write(xml)
