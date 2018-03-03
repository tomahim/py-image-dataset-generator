import argparse
import warnings

from augmentation.augmentation import DatasetGenerator
from augmentation_config import *

warnings.filterwarnings("ignore")

DEFAULT_DOWNLOAD_LIMIT = 50
DEFAULT_OUTPUT_FOLDER = "/output"

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('-folder',
                        help='Folder input path containing images that will be augmented',
                        required=True,
                        type=str
                        )

    parser.add_argument('-limit',
                        '-l',
                        help='Number of files to generate (default: %s)'
                             % DEFAULT_DOWNLOAD_LIMIT,
                        required=True,
                        type=int
                        )

    parser.add_argument('-dest',
                        '-d',
                        help='Folder destination for augmented image. (default: [folder input path] + %s)'
                        % DEFAULT_OUTPUT_FOLDER,
                        type=str,
                        default=None
                        )

    args = parser.parse_args()

    # print(args)

    generator = DatasetGenerator(
        folder_path=args.folder,
        num_files=args.limit,
        folder_destination=args.folder + DEFAULT_OUTPUT_FOLDER if args.dest is None else args.dest)

    if 'rotate' in DEFAULT_OPERATIONS:
        generator.rotate(probability=DEFAULT_ROTATE_PROBABILITY,
                         max_left_degree=DEFAULT_ROTATE_MAX_LEFT_DEGREE,
                         max_right_degree=DEFAULT_ROTATE_MAX_RIGHT_DEGREE)

    if 'blur' in DEFAULT_OPERATIONS:
        generator.blur(probability=DEFAULT_BLUR_PROBABILITY)

    if 'random_noise' in DEFAULT_OPERATIONS:
        generator.random_noise(probability=DEFAULT_RANDOM_NOISE_PROBABILITY)

    if 'horizontal_flip' in DEFAULT_OPERATIONS:
        generator.horizontal_flip(probability=DEFAULT_HORIZONTAL_FLIP_PROBABILITY)

    if 'vertical_flip' in DEFAULT_OPERATIONS:
        generator.vertical_flip(probability=DEFAULT_VERTICAL_FLIP_PROBABILITY)

    generator.execute()
