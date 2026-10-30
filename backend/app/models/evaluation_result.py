"""A shared data model for one evaluator's result."""

from dataclasses import dataclass


@dataclass
class EvaluationResult:
    """Store the outcome reported by one evaluator."""

    evaluator_name: str
    passed: bool
    reason: str
    severity: str
