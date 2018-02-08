# Python image dataset generator

This project intend to collect large images dataset with minimal effort.

First grab image from internet by specifying keywords (google images by default) and then generate new one from existing an existing dataset.

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
