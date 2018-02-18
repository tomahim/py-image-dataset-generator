# Python image dataset generator

This project intend to collect large dataset of images with minimal effort.

It could first grab image from internet by specifying keywords (Google images or Bing for now) and then generate new one from an existing dataset (not implemented yet).

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
python dataset_generator.py "red car" -limit 50 -dest images -size large
```
    
In this example, you will have 50 images of red cars in your /images/red_car folder. 

Here is the full command line usage description : 

```
python dataset_generator.py --help
usage: dataset_generator.py [-h] [-dest DEST] [-limit LIMIT] [-size SIZE]
                            [-source SOURCES] [-allsources]
                            image_keyword

positional arguments:
  image_keyword         keyword to search

optional arguments:
  -h, --help             show this help message and exit
  -dest DEST, -d DEST    Folder destination (default: images/). A sub folder is
                         created for each keywords
  -limit LIMIT, -l LIMIT Number of files to download (default: 50)
  -size SIZE, -s SIZE    Size of image to download : large,small (default:
                         large)
                        
  -resize RESIZE         Resize the downloaded image in a specific size.
                         Example: --resize=32,32 will output a 32px x 32px file
                        
  -source SOURCES, -src  SOURCES
                         Data source for download : Bing, Google (default:
                         Google)
                        
  -allsources, -as       If you want your images mixed from all download
                         sources : Bing, Google
```

### Common issues

**WebDriverException: Message: unknown error: cannot find Chrome binary**

Make sure chromedriver is well installed on your PATH (run the `which chromedriver` command on Linux and then `echo $PATH`). Also Chrome should be installed on your machine (or the `chromium-package` for Linux).

You can install the chromedriver with this command ([more information here](https://pypi.python.org/pypi/chromedriver_installer)):
`pip install chromedriver_installer --install-option="--chromedriver-version=2.35"`
