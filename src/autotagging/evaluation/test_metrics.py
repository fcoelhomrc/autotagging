import torch
import pytest

from metrics import ClassifierEvaluator


@pytest.fixture
def evaluator() -> ClassifierEvaluator:
    return ClassifierEvaluator(
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


def test_evaluator_multiple_updates(evaluator: ClassifierEvaluator):
    batch_size = 2
    for _ in range(3):
        preds = {
            "color": torch.sigmoid(torch.randn(batch_size, 10)),
            "category": torch.randn(batch_size, 20).softmax(-1),
            "status": torch.randn(batch_size, 5).softmax(-1),
        }
        target = {
            "color": (torch.rand(batch_size, 10) > 0.7).to(int),
            "category": torch.randint(0, 20, (batch_size,)),
            "status": torch.randint(0, 5, (batch_size,)),
        }
        evaluator.update(preds, target)

    results = evaluator.compute()
    assert len(results) == 11  # 2 color + 6 category + 3 status


def test_reset(evaluator: ClassifierEvaluator):
    # perfect predictions → high scores
    preds = {
        "color": torch.full((2, 10), 0.9),                 # >0.5 → 1
        "category": torch.eye(2, 20),                      # one-hot
        "status": torch.eye(2, 5),
    }
    target = {
        "color": torch.ones((2, 10)).to(int),
        "category": torch.zeros(2, dtype=torch.long),
        "status": torch.zeros(2, dtype=torch.long),
    }

    evaluator.update(preds, target)
    before = evaluator.compute()
    assert before["color_jaccard_macro"] > 0.0

    evaluator.reset()
    after = evaluator.compute()

    # after reset most metrics are NaN or 0 (depends on torchmetrics version)
    assert after["color_jaccard_macro"] == 0.0 or torch.isnan(
        torch.tensor(after["color_jaccard_macro"])
    )