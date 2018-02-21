from abc import abstractmethod, ABCMeta
from scipy import ndimage

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
    def execute(self, file_path: str):
        pass


class RotateLeft(Operation):
    degree = None

    def __init__(self, probability: float, degree: float) -> None:
        super().__init__(probability)
        self.degree = degree

    def execute(self, file_path: str):
        image = FileUtil.open(file_path)
        return rotate(image, self.degree)


class Blur(Operation):
    intensity = None

    def __init__(self, probability: float, intensity: float) -> None:
        super().__init__(probability)
        self.intensity = intensity

    def execute(self, file_path: str):
        image = FileUtil.open(file_path)
        return ndimage.uniform_filter(image, size=(11, 11, 1))


class OperationPipeline:
    operations = []

    def blur(self, probability: float, intensity: float):
        self.__add_operation(Blur(probability, intensity))

    def rotate_left(self, probability: float, degree: float):
        self.__add_operation(RotateLeft(probability, degree))

    def __add_operation(self, operation: Operation):
        self.operations.append(operation)
