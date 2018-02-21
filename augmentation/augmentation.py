import random
import os

from augmentation.operations import OperationPipeline
from utils.utils import FileUtil


class DatasetGenerator(OperationPipeline):
    folder_path = None
    max_files = None
    save_to_disk = True
    folder_destination = "result"

    def __init__(self,
                 folder_path: str,
                 max_files: int = 50,
                 save_to_disk=True,
                 folder_destination="result") -> None:
        super().__init__()
        self.folder_path = folder_path
        self.max_files = max_files
        self.save_to_disk = save_to_disk
        self.folder_destination = folder_destination

    def preview(self):
        """
            It print a preview of :
                - dataset current size
                - operations list
                - dataset augmented size
        """
        pass

    def execute(self):
        """
            Execute the pipeline operation as configured
        """
        for file in os.listdir(self.folder_path):
            file_path = os.path.join(self.folder_path, file)
            if FileUtil.is_image(file_path):
                for operation in self.operations:
                    random_num = random.uniform(0, 1)
                    do_operation = random_num <= operation.probability
                    if do_operation:
                        augmented_image = operation.execute(file_path)
                        if self.save_to_disk:
                            FileUtil.save_file(augmented_image, self.folder_destination, "aug")
