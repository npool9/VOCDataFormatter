# VOC PASCAL Data Formatter

This project takes any image dataset that you have and converts its format into VOC PASCAL format.
This becomes useful when implementing image classification/object detection methods submitted to the VOC PASCAL competitions.
Putting the image data in the format allows the development kit's evaluation functions to recognize the annotations of the images including their classes.

#### Assumptions:
1. Your own image dataset is separated into subdirectories corresponding to the class to which they belong.
2. You have the VOCdevkit directory downloaded: http://host.robots.ox.ac.uk/pascal/VOC/voc2010/VOCdevkit_08-May-2010.tar
    * You do not need the VOC PASCAL dataset provided you have your own dataset. You just need the development kit file system.
3. There is one object per image.
    * For classification purposes, the "bounding box" is just the border of the entire image.
    * These assumptions can be edited in the annotatoin_maker.py script.
    
#### Object Detection:
The default parameters of this project assume the image classification task. To perform object detection, some edits need to be made. Here are my recommendations:
1. Provide your own list of bounding boxes in the form of a list of list of lists structure.
   * You will have to write your own loop through this data stucture in the annotations_maker.py script.
   * Have the outermost list be the essentially a list of images
   * The images can be represented by lists of bounding boxes
   * The bounding boxes should be lists of the form [xmax, xmin, ymax, ymin]
      ** xml_writer function takes a list of lists as input (i.e. a list of all bounding boxes in the image)
