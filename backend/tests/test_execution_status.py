from backend.app.evaluators.execution_status import classify_execution_status


def test_classify_execution_status_returns_technical_success_for_success():
    assert classify_execution_status("success") == "TECHNICAL_SUCCESS"


def test_classify_execution_status_returns_technical_failure_for_error():
    assert classify_execution_status("error") == "TECHNICAL_FAILURE"


def test_classify_execution_status_returns_unknown_for_other_values():
    assert classify_execution_status("waiting") == "UNKNOWN_STATUS"
