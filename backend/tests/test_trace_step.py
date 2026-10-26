from backend.app.models.trace_step import TraceStep


def test_trace_step_stores_all_supplied_values():
    step = TraceStep(
        node_name="Send invoice",
        target_system="Accounting API",
        operation="create_invoice",
        status="success",
    )

    assert step.node_name == "Send invoice"
    assert step.target_system == "Accounting API"
    assert step.operation == "create_invoice"
    assert step.status == "success"


def test_trace_steps_can_store_different_operations_independently():
    first_step = TraceStep("Fetch order", "Store API", "get_order", "success")
    second_step = TraceStep("Notify customer", "Email API", "send_email", "error")

    assert first_step.operation == "get_order"
    assert second_step.operation == "send_email"
    assert first_step.operation != second_step.operation
