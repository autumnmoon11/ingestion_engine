import pytest
from engine import filter_data

def test_filter_data_excludes_blocked_ids():
    # Arrange: Set up a small mock stream and a blocked set
    mock_stream = [
        {"id": "101", "name": "Valid Item"},
        {"id": "102", "name": "Blocked Item"},
        {"id": "103", "name": "Another Valid Item"}
    ]
    blocked_ids = {"102"}

    # Act: Process the stream through our generator
    result = list(filter_data(mock_stream, blocked_ids))

    # Assert: Verify the blocked item is gone and valid ones remain
    assert len(result) == 2
    assert result[0]["id"] == "101"
    assert result[1]["id"] == "103"
    # Ensure the blocked ID is truly nowhere in the result
    assert not any(row["id"] == "102" for row in result)

def test_filter_data_handles_empty_stream():
    # Arrange
    mock_stream = []
    blocked_ids = {"123"}

    # Act
    result = list(filter_data(mock_stream, blocked_ids))

    # Assert
    assert result == []