# Python image dataset generator

This project intend to collect large dataset of images with minimal effort.

It could first grab image from internet by specifying keywords (google images for now) and then generate new one from existing an existing dataset (to implement).

### Pre-requirements

Get python dependencies

`pip install -r requirements.txt`

Run this command to install selenium Chromedriver (needed to grab images)

`python setup.py install --chromedriver-version=2.20`

### Usage

Git clone the project
cd to the root of the project
Automatically grab images with this command line :

`python dataset_generator.py "red car" -limit 50 -dest images`
    
In this example, you will have 50 images of red cars in your /images/red_car folder. 
