from __future__ import annotations

from typing import Dict, Any

import torch
from torchmetrics import MetricCollection
from torchmetrics.classification import (
    MultilabelJaccardIndex,
    MulticlassAccuracy,
    MulticlassCohenKappa,
)

from abc import ABC, abstractmethod


class Evaluator(ABC):
    """Abstract interface for all evaluators."""

    @abstractmethod
    def update(self, preds: Dict[str, torch.Tensor], target: Dict[str, torch.Tensor]) -> None:
        ...

    @abstractmethod
    def compute(self) -> Dict[str, Any]:
        ...

    @abstractmethod
    def reset(self) -> None:
        ...


class ClassifierEvaluator(Evaluator):
    """
    Multi-task evaluator for:
      • multilabel colors  → Jaccard (IoU)
      • multiclass category → top-k accuracy
      • ordinal status      → accuracy + quadratic Cohen-Kappa
    """

    def __init__(
        self,
        color_num_labels: int,
        category_num_classes: int,
        status_num_classes: int = 5,
        *,
        color_threshold: float = 0.5,
    ) -> None:
        self.color_num_labels = color_num_labels
        self.category_num_classes = category_num_classes
        self.status_num_classes = status_num_classes
        self.color_threshold = float(color_threshold)

        self.color_metrics = MetricCollection(
            {
                "color_jaccard_macro": MultilabelJaccardIndex(
                    num_labels=color_num_labels,
                    threshold=color_threshold,          
                    average="macro",
                ),
                "color_jaccard_perLabel": MultilabelJaccardIndex(
                    num_labels=color_num_labels,
                    threshold=color_threshold,
                    average="none",
                ),
            }
        )

        self.category_metrics = MetricCollection(
            {
                "category_acc_macro": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=1, average="macro"
                ),
                "category_acc_perClass": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=1, average="none"
                ),
                "category_accTop3_macro": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=3, average="macro"
                ),
                "category_accTop3_perClass": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=3, average="none"
                ),
                "category_accTop5_macro": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=5, average="macro"
                ),
                "category_accTop5_perClass": MulticlassAccuracy(
                    num_classes=category_num_classes, top_k=5, average="none"
                ),
            }
        )

        self.status_metrics = MetricCollection(
            {
                "status_acc_macro": MulticlassAccuracy(
                    num_classes=status_num_classes, top_k=1, average="macro"
                ),
                "status_acc_perClass": MulticlassAccuracy(
                    num_classes=status_num_classes, top_k=1, average="none"
                ),
                "status_qwk": MulticlassCohenKappa(
                    num_classes=status_num_classes, weights="quadratic"
                ),
            }
        )

        # master collection 
        self._all_metrics = MetricCollection(
            [self.color_metrics, self.category_metrics, self.status_metrics]
        )



    def update(self, preds: Dict[str, torch.Tensor], target: Dict[str, torch.Tensor]) -> None:
        """Feed one batch to every metric."""

        if "color" in preds and "color" in target:
            self.color_metrics.update(preds["color"], target["color"])


        if "category" in preds and "category" in target:
            self.category_metrics.update(preds["category"], target["category"])

        if "status" in preds and "status" in target:
            self.status_metrics.update(preds["status"], target["status"])


    def compute(self) -> Dict[str, Any]:
        """Return a *flat* dict with all metric values."""
        raw = self._all_metrics.compute()

        flat: Dict[str, Any] = {}
        for group in (self.color_metrics, self.category_metrics, self.status_metrics):
            # each group is a sub-dict inside `raw`
            for name, value in group.compute().items():
                # tensors → python scalar (for JSON logging, etc.)
                flat[name] = value.item() if isinstance(value, torch.Tensor) and value.size == 1 else value
        return flat


    def reset(self) -> None:
        """Reset internal metric states - call at the start of each epoch."""
        self._all_metrics.reset()



if __name__ == "__main__":
    from rich import print 

    evaluator = ClassifierEvaluator(
            color_num_labels=10,
            category_num_classes=20,
            status_num_classes=5,
        )


    def test_evaluator_update_and_compute(evaluator: ClassifierEvaluator):
        batch_size = 4

        preds = {
            "color": torch.sigmoid(torch.randn(batch_size, 10)),          # probs
            "category": torch.randn(batch_size, 20).softmax(dim=-1),      # probs
            "status": torch.randn(batch_size, 5).softmax(dim=-1),         # probs
        }

        target = {
            "color": (torch.rand(batch_size, 10) > 0.5).to(int),          # 0/1
            "category": torch.randint(0, 20, (batch_size,)),              # class index
            "status": torch.randint(0, 5, (batch_size,)),                 # class index
        }


        for key, value in preds.items():
            print(key, value.shape)

        evaluator.update(preds, target)
        results = evaluator.compute()

        expected_keys = {
            "color_jaccard_macro",
            "color_jaccard_perLabel",
            "category_acc_macro",
            "category_acc_perClass",
            "category_accTop3_macro",
            "category_accTop3_perClass",
            "category_accTop5_macro",
            "category_accTop5_perClass",
            "status_acc_macro",
            "status_acc_perClass",
            "status_qwk",
        }
        assert set(results) == expected_keys

        # sanity checks
        assert 0.0 <= results["color_jaccard_macro"] <= 1.0
        assert results["color_jaccard_perLabel"].shape == (10,)
        assert 0.0 <= results["category_acc_macro"] <= 1.0
        assert results["category_acc_perClass"].shape == (20,)

        return results 

    results = test_evaluator_update_and_compute(evaluator)  
    print(results)