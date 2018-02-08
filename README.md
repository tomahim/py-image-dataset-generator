# Python image dataset generator

This project intend to collect large dataset of images with minimal effort.

It could first grab image from internet by specifying keywords (google images for now) and then generate new one from an existing dataset (not implemented yet).

### Pre-requirements

This project is tested with Python 2.7.14.

### Installation

Git clone the project

Get the python dependencies

`pip install -r requirements.txt`

Run this command to install selenium Chromedriver (needed to grab images)

`pip install chromedriver_installer --install-option="--chromedriver-version=2.20`
or 
`pip install chromedriver_installer --install-option="--chromedriver-version=2.35` (for Bing)

### Usage

Automatically grab images with this command line (from the root of the project) :

`python dataset_generator.py "red car" -limit 50 -dest images`
    
In this example, you will have 50 images of red cars in your /images/red_car folder. 
