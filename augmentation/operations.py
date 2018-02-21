from abc import abstractmethod, ABCMeta
from sci    py import ndimage

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
