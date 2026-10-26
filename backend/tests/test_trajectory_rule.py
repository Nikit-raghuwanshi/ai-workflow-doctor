from backend.app.evaluators.trajectory_rule import evaluate_trajectory


def test_trajectory_passes_for_an_exact_match():
    result = evaluate_trajectory(["Start", "Validate", "Finish"], ["Start", "Validate", "Finish"])

    assert result == {
        "passed": True,
        "missing_steps": [],
        "extra_steps": [],
        "order_correct": True,
    }


def test_trajectory_fails_when_a_required_step_is_missing():
    result = evaluate_trajectory(["Start", "Validate", "Finish"], ["Start", "Finish"])

    assert result == {
        "passed": False,
        "missing_steps": ["Validate"],
        "extra_steps": [],
        "order_correct": False,
    }


def test_trajectory_fails_when_an_extra_step_occurs():
    result = evaluate_trajectory(["Start", "Finish"], ["Start", "Notify", "Finish"])

    assert result == {
        "passed": False,
        "missing_steps": [],
        "extra_steps": ["Notify"],
        "order_correct": False,
    }


def test_trajectory_fails_when_steps_are_in_the_wrong_order():
    result = evaluate_trajectory(["Start", "Validate", "Finish"], ["Start", "Finish", "Validate"])

    assert result == {
        "passed": False,
        "missing_steps": [],
        "extra_steps": [],
        "order_correct": False,
    }


def test_trajectory_fails_when_a_step_is_duplicated():
    result = evaluate_trajectory(["Start", "Finish"], ["Start", "Finish", "Finish"])

    assert result == {
        "passed": False,
        "missing_steps": [],
        "extra_steps": ["Finish"],
        "order_correct": False,
    }


def test_trajectory_passes_for_two_empty_lists():
    result = evaluate_trajectory([], [])

    assert result == {
        "passed": True,
        "missing_steps": [],
        "extra_steps": [],
        "order_correct": True,
    }
