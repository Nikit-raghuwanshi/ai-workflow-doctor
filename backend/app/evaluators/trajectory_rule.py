"""Evaluate whether workflow nodes followed an expected trajectory."""

from collections import Counter


def evaluate_trajectory(expected_steps, actual_steps):
    """Compare ordered node-name lists and report trajectory differences."""
    expected_counts = Counter(expected_steps)
    actual_counts = Counter(actual_steps)

    missing_steps = []
    for step in expected_steps:
        if actual_counts[step] < expected_counts[step]:
            missing_steps.append(step)
            actual_counts[step] += 1

    extra_steps = []
    for step in actual_steps:
        if expected_counts[step] < actual_counts[step]:
            extra_steps.append(step)
            expected_counts[step] += 1

    order_correct = expected_steps == actual_steps
    passed = not missing_steps and not extra_steps and order_correct

    return {
        "passed": passed,
        "missing_steps": missing_steps,
        "extra_steps": extra_steps,
        "order_correct": order_correct,
    }
