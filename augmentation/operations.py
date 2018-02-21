from abc import abstractmethod, ABCMeta
from scipy import ndimage, ndarray

from skimage.transform import rotate

from utils.utils import FileUtil


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


class RotateLeft(Operation):
    degree = None

    def __init__(self, probability: float, degree: float) -> None:
        super().__init__(probability)
        self.degree = degree

    def execute(self, image_array: ndarray):
        return rotate(image_array, self.degree)


class Blur(Operation):
    intensity = None

    def __init__(self, probability: float, intensity: float) -> None:
        super().__init__(probability)
        self.intensity = intensity

    def execute(self, image_array: ndarray):
        return ndimage.uniform_filter(image_array, size=(11, 11, 1))


class OperationPipeline:
    operations = []

    def blur(self, probability: float, intensity: float):
        self.__add_operation(Blur(probability, intensity))

    def rotate_left(self, probability: float, degree: float):
        self.__add_operation(RotateLeft(probability, degree))

    def __add_operation(self, operation: Operation):
        self.operations.append(operation)
