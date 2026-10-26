from backend.app.evaluators.read_only_rule import evaluate_read_only_rule
from backend.app.models.trace_step import TraceStep


def test_read_operation_passes_the_read_only_rule():
    step = TraceStep("Get order", "Store API", "read", "success")

    result = evaluate_read_only_rule(step)

    assert result == {"passed": True, "reason": "'read' is allowed in read-only mode."}


def test_update_operation_fails_the_read_only_rule():
    step = TraceStep("Update order", "Store API", "update", "success")

    result = evaluate_read_only_rule(step)

    assert result == {"passed": False, "reason": "'update' is not approved in read-only mode."}


def test_delete_operation_fails_the_read_only_rule():
    step = TraceStep("Delete order", "Store API", "delete", "success")

    result = evaluate_read_only_rule(step)

    assert result == {"passed": False, "reason": "'delete' is not approved in read-only mode."}


def test_uppercase_update_operation_fails_the_read_only_rule():
    step = TraceStep("Update order", "Store API", "UPDATE", "success")

    result = evaluate_read_only_rule(step)

    assert result == {"passed": False, "reason": "'UPDATE' is not approved in read-only mode."}


def test_uppercase_get_operation_passes_the_read_only_rule():
    step = TraceStep("Get order", "Store API", "GET", "success")

    result = evaluate_read_only_rule(step)

    assert result == {"passed": True, "reason": "'GET' is allowed in read-only mode."}


def test_unknown_operation_fails_the_read_only_rule():
    step = TraceStep("Send invoice", "Email API", "send_email", "success")

    result = evaluate_read_only_rule(step)

    assert result == {
        "passed": False,
        "reason": "'send_email' is not approved in read-only mode.",
    }
