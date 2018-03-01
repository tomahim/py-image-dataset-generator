from abc import abstractmethod, ABCMeta
import random

from scipy import ndimage, ndarray
from skimage.transform import rotate, resize
from skimage.util import random_noise


class Operation:
    __metaclass__ = ABCMeta

    probability = 1

    @abstractmethod
    def __init__(self, probability: float) -> None:
        super().__init__()
        self.probability = probability

    @abstractmethod
    def execute(self, image_array: ndarray):
        pass


class Rotate(Operation):
    max_left_degree = None
    max_right_degree = None

    def __init__(self, probability: float, max_left_degree: int, max_right_degree: int) -> None:
        super().__init__(probability)
        self.max_left_degree = max_left_degree
        self.max_right_degree = max_right_degree

    def execute(self, image_array: ndarray):
        random_degree = random.uniform(-self.max_right_degree, self.max_left_degree)
        return rotate(image_array, random_degree)


class RandomNoise(Operation):
    def __init__(self, probability: float) -> None:
        super().__init__(probability)

    def execute(self, image_array: ndarray):
        return random_noise(image_array)


class Blur(Operation):
    width = None
    height = None

    def __init__(self, probability: float) -> None:
        super().__init__(probability)

    def execute(self, image_array: ndarray):
        return ndimage.uniform_filter(image_array, size=(11, 11, 1))


class Resize(Operation):
    def __init__(self, probability: float, width: int, height: int) -> None:
        super().__init__(probability)
        self.width = width
        self.height = height

    def execute(self, image_array: ndarray):
        return resize(image_array, (self.width, self.height))


class HorizontalFlip(Operation):

    def __init__(self, probability: float) -> None:
        super().__init__(probability)

    def execute(self, image_array: ndarray):
        return image_array[:, ::-1]


class VerticalFlip(Operation):

    def __init__(self, probability: float) -> None:
        super().__init__(probability)

    def execute(self, image_array: ndarray):
        return image_array[::-1, :]


class OperationPipeline:
    operations = []

    def blur(self, probability: float):
        self.__add_operation(Blur(probability))

    def rotate(self, probability: float, max_left_degree: int, max_right_degree: int):
        self.__add_operation(Rotate(probability, max_left_degree, max_right_degree))

    def random_noise(self, probability: float):
        self.__add_operation(RandomNoise(probability))

    def resize(self, probability: float, width: int, height: int):
        self.__add_operation(Resize(probability, width, height))

    def horizontal_flip(self, probability: float):
        self.__add_operation(HorizontalFlip(probability))

    def vertical_flip(self, probability: float):
        self.__add_operation(VerticalFlip(probability))

    def __add_operation(self, operation: Operation):
        self.operations.append(operation)
