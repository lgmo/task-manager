from typing import Any

import pytest


@pytest.fixture
def task_data() -> dict[str, Any]:
    return {
        "title": "Title",
        "description": "Description",
        "status": "todo",
    }
