from torchmetrics import (
    JaccardIndex, Accuracy, 
)


from pydantic import BaseModel
from enum import Enum 


class Color(Enum):
    BLUE = "blue"
    RED = "red"


class ClassificationOutput(BaseModel):
    category: int
    status: int
    color: list[Color]






class ClassificationMetrics:
    
    def __init__(self):
        
        pass 

    def update():


    





# JACARD INDEX 
# INTERSECTION(A, B) / UNION(A, B)
# Use fixed set infered from dataset 

# Big black jacket with small red stamp

# GT: [Black, Red]
# PRED: [Black]
# JacIndex: [Black] / [Black, Red] = 1/2 = 0.50

# GT: [Black, Red]
# PRED: [Red]
# JacIndex: [Red] / [Black, Red] = 1/2 = 0.50


# GT: [Black, Red]
# PRED: [Black, Light Red, Deep Red, Red, Tomato Red]
# JacIndex: [Black] / [...] = 1/5 = 0.20



# GT: [Black, Red]
# PRED: [Blue]
# JacIndex: [] / [Black, Red, Blue] = 0.0


# BRANDS
# NO LABEL -> (There is no label / User omitted label but it appears in image and is indexed / The label appears but not indexed by Vinted)

# Matching  (GT == Pred) -> Acc %     75%


# Adidas, Nike, Apple + (NO LABEL)
# Input: Tesla

# Output: X 
# Check X against allowed values (infered from dataset) -> if NO LABEL, skip 


# Outputs
# --> brand_is_visible: bool 
# --> brand: str (if brand_is_visible else) None


# CASE 1  (OK) 
# ground truth -> NO LABEL 
# brand_is_visible: False
# brand -> NO LABEL 


# CASE 2
# ground truth -> NO LABEL 
# brand_is_visible: True
# brand



# Subset: brand != NO LABEL
# --> How well model predicts non-ambiguous case? 
# --> Convert text to integer label 
# ACC% = 80%    20%       Limitation: cannot differentiate between (model failed / information not available on images / noisy brand ground truth)
# Record mistakes for manual inspection -> (model failed / information not available)

# Subset: brand == NO LABEL 
# Case 1. There IS NO brand in the image
# Case 2. There IS a brand in the image, but it does not match any Vinted brands, so it ends up as NO LABEL 
# --> 
# Record cases where model thinks brand_is_visible (so we can check if info was indeed visible)
# Implement test suite 



# The label appears but not indexed by Vinted
# User omitted label but it appears in image and is indexed
# GT: NO LABEL
# Pred: something