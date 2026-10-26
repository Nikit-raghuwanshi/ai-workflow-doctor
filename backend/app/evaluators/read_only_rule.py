"""Evaluate whether one recorded operation respects the read-only rule."""

from backend.app.models.trace_step import TraceStep


def evaluate_read_only_rule(step: TraceStep):
    """Return whether a trace step's operation is allowed in read-only mode."""
    allowed_operations = {"read", "get", "list", "search"}

    if step.operation.lower() in allowed_operations:
        return {
            "passed": True,
            "reason": f"'{step.operation}' is allowed in read-only mode.",
        }

    return {
        "passed": False,
        "reason": f"'{step.operation}' is not approved in read-only mode.",
    }
