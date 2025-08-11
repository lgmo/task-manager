from typing import Any

import pytest

from accounts.models import UserModel


@pytest.fixture
def task_data() -> dict[str, Any]:
    return {
        "title": "Title",
        "description": "Description",
        "status": "todo",
    }


@pytest.fixture
def user() -> UserModel:
    return UserModel.objects.create()
