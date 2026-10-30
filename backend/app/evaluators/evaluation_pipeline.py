"""Combine the small workflow evaluators into one deterministic result."""

from backend.app.evaluators.execution_status import classify_execution_status
from backend.app.evaluators.read_only_rule import evaluate_read_only_rule
from backend.app.evaluators.trajectory_rule import evaluate_trajectory
from backend.app.models.evaluation_result import EvaluationResult


def evaluate_workflow_execution(workflow_status, trace_steps, expected_node_names):
    """Evaluate a workflow status, operations, and node trajectory together.

    Failed execution and trajectory checks are high severity. Unauthorized
    operations are critical. Every passed check has low severity.
    """
    execution_result = _evaluate_execution_status(workflow_status)
    read_only_result = _evaluate_read_only_operations(trace_steps)
    trajectory_result = _evaluate_node_trajectory(trace_steps, expected_node_names)

    results = [execution_result, read_only_result, trajectory_result]

    return {
        "passed": all(result.passed for result in results),
        "results": results,
    }


def _evaluate_execution_status(workflow_status):
    """Convert the execution-status evaluator output into a shared result."""
    status_classification = classify_execution_status(workflow_status)

    if status_classification == "TECHNICAL_SUCCESS":
        return EvaluationResult(
            "execution_status",
            True,
            "Execution status is technically successful.",
            "low",
        )

    if status_classification == "TECHNICAL_FAILURE":
        return EvaluationResult(
            "execution_status",
            False,
            "Execution status indicates a technical failure.",
            "high",
        )

    return EvaluationResult(
        "execution_status",
        False,
        f"Execution status '{workflow_status}' is not a technical success.",
        "high",
    )


def _evaluate_read_only_operations(trace_steps):
    """Fail when any recorded step violates the existing read-only rule."""
    failure_reasons = []

    for step in trace_steps:
        rule_result = evaluate_read_only_rule(step)
        if not rule_result["passed"]:
            failure_reasons.append(f"Node '{step.node_name}': {rule_result['reason']}")

    if failure_reasons:
        return EvaluationResult(
            "read_only_rule",
            False,
            " ".join(failure_reasons),
            "critical",
        )

    return EvaluationResult(
        "read_only_rule",
        True,
        "All recorded operations are allowed in read-only mode.",
        "low",
    )


def _evaluate_node_trajectory(trace_steps, expected_node_names):
    """Convert the trajectory evaluator output into a shared result."""
    actual_node_names = [step.node_name for step in trace_steps]
    trajectory = evaluate_trajectory(expected_node_names, actual_node_names)

    if trajectory["passed"]:
        return EvaluationResult(
            "trajectory_rule",
            True,
            "Workflow steps match the expected trajectory.",
            "low",
        )

    reasons = []
    if trajectory["missing_steps"]:
        reasons.append(f"Missing steps: {', '.join(trajectory['missing_steps'])}.")
    if trajectory["extra_steps"]:
        reasons.append(f"Extra steps: {', '.join(trajectory['extra_steps'])}.")
    if not trajectory["order_correct"]:
        reasons.append("Workflow steps do not exactly match the expected order.")

    return EvaluationResult("trajectory_rule", False, " ".join(reasons), "high")
