from backend.app.models.evaluation_result import EvaluationResult


def test_evaluation_result_stores_all_supplied_values():
    result = EvaluationResult(
        evaluator_name="read_only_rule",
        passed=False,
        reason="'update' is not approved in read-only mode.",
        severity="high",
    )

    assert result.evaluator_name == "read_only_rule"
    assert result.passed is False
    assert result.reason == "'update' is not approved in read-only mode."
    assert result.severity == "high"


def test_evaluation_results_store_independent_values():
    passing_result = EvaluationResult("trajectory_rule", True, "Steps match.", "low")
    failing_result = EvaluationResult("read_only_rule", False, "Update found.", "high")

    assert passing_result.passed is True
    assert failing_result.passed is False
    assert passing_result.evaluator_name != failing_result.evaluator_name
    assert passing_result.reason != failing_result.reason
