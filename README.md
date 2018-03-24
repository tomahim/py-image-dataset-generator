# Image dataset generator for Deep learning projects

[![Join the chat at https://gitter.im/py-image-dataset-generator/Lobby](https://badges.gitter.im/py-image-dataset-generator/Lobby.svg)](https://gitter.im/py-image-dataset-generator/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

### Get a large image dataset with minimal effort

This tool **automatically collect images** from Google or Bing and optionally resize them. 

```
python download.py "funny cats" -limit=100 -dest=folder_name -resize=250x250
```

Then you can **randomly generate new images** with image augmentation from an existing folder. It will add noise, rotate, transform, flip, blur on random images.

```
python augmentation.py -folder=my_folder/funny_cats -limit=10000
```

TADA ! In few seconds you will get 10 000 different images of funny cats to train your favorite deep learning algorithm !

### Table of content

* [Pre-requirements](#pre-requirements)
* [Installation](#installation)
* [Run unit tests](#run-unit-tests)
* [Usage](#usage)
    * [Download images](#download-images-from-the-web)
    * [Image augmentation](#image-augmentation)
    * [Create a custom image augmentation pipeline](#create-a-custom-image-augmentation-pipeline)
* [Common issues](#common-issues)
* [Acknowledgments](#acknowledgments)

### Pre-requirements

This project is tested with Python 3.6.4 and more.

*Linux*

- chromium-browser package (`sudo apt-get install chromium-browser`)

*Windows*

- Chrome should be installed
- [Microsoft Visual C++ Build Tools](https://www.scivision.co/python-windows-visual-c++-14-required/) (scikit image dependency, [see for more info](https://www.scivision.co/python-windows-visual-c++-14-required/))

### Installation

Git clone the project

Get the python dependencies

```
pip install -r requirements.txt
```

### Run unit tests

```
python -m unittest discover
```

### Usage

#### Download images from the web

```
python download.py "red car" -limit=150 -dest=folder_name -resize=250x250
```
    
After running this command, you will have 150 images of *red cars* (resized 250px by 250px) in the /folder_name/red_car folder. 

You can find all possible parameters in the table below (also available with the `--help` parameter) :

Parameters  | Description
---    | --- 
Keyword *(required)* | The first parameter should be a keyword describing the images to search for. <br><br> `python download.py "red car"`
Destination folder <br>*-dest or -d* | Specify the destination folder to save files (default: images/) <br><br> `python download.py "red car" -dest=your_folder`
Limit number <br>*-limit or -l* | Specify the number of files to download (default: 50). See the note below for the maximum limit. <br><br> `python download.py "red car" -limit=200`
Thumbnail only <br>*-thumbnail or -thumb* | Download the thumbnail instead of the full original image <br><br>   `python download.py "red car" -thumbnail`
Resize image <br>*-resize* | Resize downloaded images on the fly, to get a dataset formatted with the same size (default: no resizing). The parameter should be a couple of number representing the width and height (32x32 will ouput 32px x 32px image files) <br><br>  `python download.py "red car" -resize=32x32"`
Grab source <br>*-source, -src or -allsources* |  Choose the website to grab images : Google and/or Bing (default: Google). *-allsources* parameter can be use to. It will equally mix image files from all available sources <br><br> `python download.py "red car" -source=Google` (single source) <br> `python download.py "red car" -source=Google -source=Bing` (multi source)<br> `python download.py "red car" -allsources` (all sources)

Note : There are known limitations for the total number of images you can download in one use of the `download.py` script. Bing and Google won't let you download more than 800 images each, so the maximum for one download is around 1600 images if you use the `-allsources` parameter.

#### Image augmentation

```
python augmentation.py -folder=your_folder -limit=10000
```

10 000 augmented images will output by default to the "output" folder inside your image folder.

By default, this command will randomly apply these image transformations :

- Blur image (with a probability of 10%)
- Add Random noise (with a probability of 50%)
- Horizontal flip (with a probability of 30%)
- Left or Right rotation between 0 or 25 degree (with a probability of 50%)

- *... to be completed*

You can customize these default values by editing the `augmentation_config.py` file or by making [your own image augmentation pipeline](#create-a-custom-image-augmentation-pipeline)

You can find all possible parameters in the table below (also available with the `--help` parameter) :

Parameters  | Description
---    | --- 
Keyword *(required)* | Folder input path containing images that will be augmented.`
Destination folder <br>*-dest or -d* | Specify the destination folder to save augmented files (default: /your_folder/output) <br><br> `python augmentation.py -folder=your_folder -limit=50 -dest=other_folder`
Limit number <br>*-limit or -l* | Number of image to generate by augmentation (default: 50)

#### Create a custom image augmentation pipeline

```python
from augmentation.augmentation import DatasetGenerator

pipeline = DatasetGenerator(
    folder_path="images/red_car/",
    max_files=5000,
    save_to_disk=True,
    folder_destination="images/red_car/results"
)
pipeline.rotate(probability=0.5, max_left_degree=25, max_right_degree=25)
pipeline.random_noise(probability=0.5)
pipeline.blur(probability=0.5)
pipeline.vertical_flip(probability=0.1)
pipeline.horizontal_flip(probability=0.2)
pipeline.resize(probability=1, width=20, height=20)
pipeline.execute()
```

That's it !

### Common issues

**WebDriverException: Message: unknown error: cannot find Chrome binary**

Make sure chromedriver is well installed on your PATH (run the `which chromedriver` command on Linux and then `echo $PATH`). Also Chrome should be installed on your machine (or the `chromium-package` for Linux).

You can install the chromedriver with this command ([more information here](https://pypi.python.org/pypi/chromedriver_installer)):
`pip install chromedriver_installer --install-option="--chromedriver-version=2.35"`

**error: Microsoft Visual C++ 14.0 is required. Get it with "Microsoft Visual C++ Build Tools": [http://landinghub.visualstudio.com/visual-cpp-build-tools](https://www.scivision.co/python-windows-visual-c++-14-required/)**

As this repo use scikit-image for image processing, on Windows you need Microsoft Visual C++ Build Tools which is provided with Visual Studio (think to check the C++ options on installation). You can install it with the link below.

### Acknowledgments

- This repo is *largely inspired* by the work of Marcus Bloice on his [Augmentor](https://arxiv.org/abs/1708.04680) project. Many thanks for the great work and the useful documentation.

- I also pick some ideas from [this great series of articles](https://www.pyimagesearch.com/2017/12/11/image-classification-with-keras-and-deep-learning/) for the *automatic* part to grab images.

The goal of this repo is mainly to provide the smaller python library as possible to generate an image dataset, without a big framework like Keras, Tflearn etc, which can be hard to configure and install for new people working on Data Science / AI.
