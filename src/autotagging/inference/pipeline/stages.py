from item import ItemData, NEREntity, ROIEntity, OCREntity, VLMEntity
from abc import ABC, abstractmethod

class AbstractStage(ABC):
    @abstractmethod
    def setup(self):
        """
        Necessary setup for the stage.
        - Model initialization
        - Loading weights
        - Any other required preparation
        """
        pass

    @abstractmethod
    def run(self, item):
        """Process an Item through the stage and return the correct Entity."""
        pass

class NERStage(AbstractStage):
    def run(self, item: ItemData):
        item.ner_output = NEREntity(size="M", brand="Nike")
        return item

class ROIStage(AbstractStage):
    def run(self, item: ItemData):
        item.roi_boxes = [ROIEntity(label="hoodie", brand="Nike")]
        return item

class OCRStage(AbstractStage):
    def run(self, item: ItemData):
        item.ocr_output = [OCREntity(size="M", brand="Nike")]
        return item

class VLMStage(AbstractStage):
    def run(self, item: ItemData):
        item.roi_boxes = [ROIEntity(label="hoodie", brand="Nike")]
        return item
