"""Small helpers for classifying a workflow execution's technical status."""


def classify_execution_status(status):
    """Return a technical classification for a raw execution status."""
    if status == "success":
        return "TECHNICAL_SUCCESS"
    if status == "error":
        return "TECHNICAL_FAILURE"
    return "UNKNOWN_STATUS"
