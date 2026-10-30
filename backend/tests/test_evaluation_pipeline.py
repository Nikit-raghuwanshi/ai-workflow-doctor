from backend.app.evaluators.evaluation_pipeline import evaluate_workflow_execution
from backend.app.models.trace_step import TraceStep


def results_by_name(pipeline_result):
    return {result.evaluator_name: result for result in pipeline_result["results"]}


def test_pipeline_passes_when_all_evaluators_pass():
    steps = [
        TraceStep("Get order", "Store API", "get", "success"),
        TraceStep("Search customer", "CRM API", "search", "success"),
    ]

    result = evaluate_workflow_execution("success", steps, ["Get order", "Search customer"])
    checks = results_by_name(result)

    assert result["passed"] is True
    assert all(check.passed for check in checks.values())
    assert all(check.severity == "low" for check in checks.values())


def test_pipeline_fails_for_an_execution_status_failure():
    steps = [TraceStep("Get order", "Store API", "get", "success")]

    result = evaluate_workflow_execution("error", steps, ["Get order"])
    checks = results_by_name(result)

    assert result["passed"] is False
    assert checks["execution_status"].passed is False
    assert checks["execution_status"].severity == "high"
    assert checks["read_only_rule"].passed is True
    assert checks["trajectory_rule"].passed is True


def test_pipeline_fails_for_an_unauthorized_operation():
    steps = [TraceStep("Update order", "Store API", "update", "success")]

    result = evaluate_workflow_execution("success", steps, ["Update order"])
    checks = results_by_name(result)

    assert result["passed"] is False
    assert checks["read_only_rule"].passed is False
    assert checks["read_only_rule"].severity == "critical"
    assert "'update' is not approved" in checks["read_only_rule"].reason


def test_pipeline_fails_for_a_missing_workflow_step():
    steps = [TraceStep("Get order", "Store API", "get", "success")]

    result = evaluate_workflow_execution("success", steps, ["Get order", "Search customer"])
    checks = results_by_name(result)

    assert result["passed"] is False
    assert checks["trajectory_rule"].passed is False
    assert checks["trajectory_rule"].severity == "high"
    assert "Missing steps: Search customer." in checks["trajectory_rule"].reason
    assert "Workflow steps do not exactly match the expected order." in checks["trajectory_rule"].reason


def test_pipeline_reports_missing_extra_and_order_mismatch_details():
    steps = [
        TraceStep("Read", "Store API", "read", "success"),
        TraceStep("Report", "Reporting API", "get", "success"),
        TraceStep("Report", "Reporting API", "get", "success"),
    ]

    result = evaluate_workflow_execution("success", steps, ["Read", "Analyze", "Report"])
    trajectory_result = results_by_name(result)["trajectory_rule"]

    assert result["passed"] is False
    assert trajectory_result.passed is False
    assert "Missing steps: Analyze." in trajectory_result.reason
    assert "Extra steps: Report." in trajectory_result.reason
    assert "Workflow steps do not exactly match the expected order." in trajectory_result.reason


def test_pipeline_reports_multiple_simultaneous_failures():
    steps = [TraceStep("Update order", "Store API", "update", "error")]

    result = evaluate_workflow_execution("error", steps, ["Get order"])
    checks = results_by_name(result)

    assert result["passed"] is False
    assert checks["execution_status"].passed is False
    assert checks["read_only_rule"].passed is False
    assert checks["trajectory_rule"].passed is False
