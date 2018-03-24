import base64
import math
import time
import urllib.request
from typing import NoReturn, Tuple

from skimage import io as _io
from skimage.transform import resize

from image_grabber.grabbed_image import GrabbedImage
from utils.utils import *
from .bing_grabber import BingGrabber
from .google_grabber import GoogleGrabber
from .grab_settings import *


class ImageDownloader:
    """Download images from a keyword and website sources"""

    keyword = None
    destination = DEFAULT_DESTINATION_FOLDER
    limit = DEFAULT_DOWNLOAD_LIMIT
    file_prefix = None
    full_image = True
    resize = None

    sources = [DEFAULT_GRAB_SOURCE_TYPE]

    def __init__(self, destination=DEFAULT_DESTINATION_FOLDER, limit=DEFAULT_DOWNLOAD_LIMIT):
        """Constructor for ImageGrabber"""
        self.destination = destination
        self.limit = limit

    def download_images(self, keyword: str) -> NoReturn:

        start_time = time.time()

        if not keyword:
            raise Exception('No keyword to search')

        self.keyword = keyword
        self.__set_default_file_prefix()
        all_sources = [e.value for e in GrabSourceType]
        selected_sources = all_sources if ALL_SOURCE in self.sources else self.sources
        images = []
        if GrabSourceType.GOOGLE.value in selected_sources:
            google_grabber = GoogleGrabber()
            google_grabber.full_image = self.full_image
            images.extend(google_grabber.get_images_url(self.keyword, self.limit))

        if GrabSourceType.BING.value in selected_sources:
            bing_grabber = BingGrabber()
            bing_grabber.full_image = self.full_image
            images.extend(bing_grabber.get_images_url(self.keyword, self.limit))

        if ALL_SOURCE in self.sources or len(selected_sources) > 1:
            images = self.__repart_between_image_sources(selected_sources, images)

        if not images:
            raise (NoImageFoundException("No images found on sources %s" % ",".join(list(self.sources))))
        else:
            sub_folder_name = self.__create_destination_folder()
            print("\n %s images found on %s, limit to download: %s \n" % (len(images), self.sources, self.limit))
            nb_downloaded = self.__download_files(images, sub_folder_name)
            end_time = time.time()
            print("\n\n %s images downloaded in %s sec" % (nb_downloaded, round(end_time - start_time, 2)))

    def __repart_between_image_sources(self, sources: List[str], images: List[GrabbedImage]) -> List[GrabbedImage]:
        nb_by_source = int(math.ceil(self.limit / len(sources)))
        repart_images = []
        for source in sources:
            repart_images.extend([img for img in images if img.source == source][:nb_by_source])
        return repart_images

    def __set_default_file_prefix(self) -> NoReturn:
        """if no specified file prefix, build one from keyword"""
        if self.file_prefix is None:
            self.file_prefix = StringUtil.underscore_and_lowercase(self.keyword)

    def __create_destination_folder(self) -> str:
        """ set default destination to 'images', create and return sub_folder based on keyword name """
        if self.destination is None:
            self.destination = 'images'

        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        sub_folder = os.path.join(self.destination, StringUtil.underscore_and_lowercase(self.keyword))

        if not os.path.exists(sub_folder):
            os.mkdir(sub_folder)
        return sub_folder

    def __download_files(self, images: List[GrabbedImage], folder_path: str) -> int:
        """urls param is a list of GrabbedImage object with url / extension or just base64"""
        nb_downloaded = 0
        for i, image in enumerate(images):
            if nb_downloaded == self.limit:
                break
            try:
                full_destination = FileUtil.generate_next_file_path(folder_path, self.file_prefix)
                if self.resize is not None:
                    self.__resize_and_save(image, self.resize, full_destination)
                else:
                    self.__save_image(image, full_destination)

                nb_downloaded = nb_downloaded + 1
                ProgressBarUtil.update(nb_downloaded, self.limit)

            except Exception as e:
                ExceptionUtil.print(e)
                pass
        return nb_downloaded

    def __save_image(self, image: GrabbedImage, full_destination: str):
        """ save base64 or file from URL on the disk """
        image_to_write = None
        if image.base64 is not None:
            image_to_write = self.__decode_base64(image.base64)
        elif image.url is not None:
            image_to_write = urllib.request.urlopen(image.url).read()

        f = open(full_destination, 'wb')
        f.write(image_to_write)
        f.close()

    def __resize_and_save(self, image: GrabbedImage, size: Tuple[int], dest: str):
        """ Resize the file with size Tuple (width, height) and save it to the destination path """
        image_url = None
        if image.url is not None:
            image_url = image.url
        elif image.base64 is not None:
            # in case of base64 content, need to physically create the file
            # the file is then overwrite with the resized image
            f = open(dest, 'wb')
            f.write(self.__decode_base64(image.base64))
            f.close()
            image_url = dest

        image_array = _io.imread(image_url)
        _io.imsave(dest, resize(image_array, size))

    def __decode_base64(self, base_64: bytes):
        return base64.decodebytes(bytes(base_64.split('base64,')[1], 'utf-8'))
