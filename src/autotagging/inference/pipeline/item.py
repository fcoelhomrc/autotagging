from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from PIL import Image

@dataclass
class NEREntity:
    size: Optional[str] = None
    brand: Optional[str] = None
    material: List[str] = field(default_factory=list)
    category: Optional[str] = None
    color: List[str] = field(default_factory=list)
    
    
@dataclass
class ROIEntity:
    label: Optional[Any] = None
    brand: Optional[Any] = None

@dataclass
class OCREntity:
    size: Optional[str] = None
    brand: Optional[str] = None
    material: List[str] = field(default_factory=list)

@dataclass
class VLMEntity:
    category: str
    color: List[str] = field(default_factory=list)


@dataclass
class ItemData:
    # Input data (Mandatory)
    title: str
    description: str
    images: List[Image.Image]
    
    # Pipeline steps
    ner_output: Optional[NEREntity] = None
    roi_boxes: Optional[ROIEntity] = None # Label, brand, ...
    ocr_output: Optional[OCREntity] = None
    vlm_output: Optional[VLMEntity] = None

    # Attributes output
    attr_json: Optional[Dict[str, Any]] = field(default_factory=dict)