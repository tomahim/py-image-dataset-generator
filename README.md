# Python image dataset generator

## Download and generate large image datasets with minimal effort

This tool automatically collect images from Google or Bing and optionaly resize them. Then you can generate new images from an existing dataset by adding noise, rotate, transform etc (developement in progress).

### Table of content

* [Pre-requirements](#pre-requirements)
* [Installation](#installation)
* [Run unit tests](#run-unit-tests)
* [Usage](#usage)
* [Common issues](#common-issues)

### Pre-requirements

This project is tested with Python 3.5.4 and more.

Chrome should be installed on *Windows* or chromium-browser package on *Linux* (`sudo apt-get install chromium-browser`)

### Installation

Git clone the project

Get the python dependencies

`pip install -r requirements.txt`

### Run unit tests

```
python -m unittest discover
```

### Usage

Automatically grab *red cars* images with this command line (from the root of the project) :

```
python dataset_generator.py "red car" -limit 150 -dest folder_name -resize=250x250
```
    
After running this command, you will have 150 images of red cars (resized 250px by 250px) in the /folder_name/red_car folder. 

You can find all possible parameters in the table below (also available with the `--help` command) :

Parameters  | Description
---    | --- 
Keyword *(required)* | The first parameter should be a keyword describing the images to search for. <br><br> `python dataset_generator.py "red car"`
Destination folder <br>*-dest or -d* | Specify the destination folder to save files (default: images/) <br><br> `python dataset_generator.py "red car" -dest=your_folder`
Limit number <br>*-limit or -l* | Specify the number of files to download (default: 50) <br><br> `python dataset_generator.py "red car" -limit 200`
Thumbnail only <br>*-thumbnail or -thumb* | Download the thumbnail instead of the full original image <br><br>   `python dataset_generator.py "red car" -thumbnail`
Resize image <br>*-resize* | Resize downloaded images on the fly, to get a dataset formatted with the same size (default: no resizing). The parameter should be a couple of number representing the width and height (32x32 will ouput 32px x 32px image files) <br><br>  `python dataset_generator.py "red car" -resize=32x32"`
Grab source <br>*-source, -src or -allsources* |  Choose the website to grab images : Google and/or Bing (default: Google). *-allsources* parameter can be use to. It will equally mix image files from all available sources <br><br> `python dataset_generator.py "red car" -source Google` (single source) <br> `python dataset_generator.py "red car" -source Google -source Bing` (multi source)<br> `python dataset_generator.py "red car" -allsources` (all sources)


### Common issues

**WebDriverException: Message: unknown error: cannot find Chrome binary**

Make sure chromedriver is well installed on your PATH (run the `which chromedriver` command on Linux and then `echo $PATH`). Also Chrome should be installed on your machine (or the `chromium-package` for Linux).

You can install the chromedriver with this command ([more information here](https://pypi.python.org/pypi/chromedriver_installer)):
`pip install chromedriver_installer --install-option="--chromedriver-version=2.35"`
