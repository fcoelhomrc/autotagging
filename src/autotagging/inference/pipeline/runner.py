from typing import List
from item import ItemData

from stages import *

class InferencePipeline:
    """
    Executes a sequence of stages on an ItemData object.
    """
    def __init__(self, x: ItemData):
        self.stages = self.get_stages()

    # TODO: Parallel execution to speed up inference (if necessary)
    def run(self, item: ItemData) -> ItemData:
        for stage in self.stages:
            stage.setup()
            stage.run(item)
        return item

    def get_stages(self):
        stages = [
            NERStage,
            ROIStage,
            OCRStage,
            VLMStage,
        ]
        return stages