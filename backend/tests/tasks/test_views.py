from datetime import datetime, timedelta
from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from accounts.models import UserModel
from tasks.models import TaskModel

# TODO: uncomment after implementing auth flows
# @pytest.mark.django_db
# def test_create_task(
#     client: APIClient,
#     user: UserModel,
#     task_data: dict[str, Any],
# ) -> None:
#     # Arrange
#     url = reverse("tasks-list")

#     # Act
#     res = client.post(path=url, data=task_data, format="json")

#     # Assert
#     assert res.status_code == status.HTTP_201_CREATED
#     res_dict = res.json()
#     task = TaskModel.objects.first()
#     assert task is not None
#     diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at # noqa: E501
#     assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
#     diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at # noqa: E501
#     assert str(task.id) == res_dict.pop("id")
#     assert res_dict == task_data


@pytest.mark.django_db
def test_list_tasks(
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
) -> None:
    # Arrange
    url = reverse("tasks-list")
    task = TaskModel.objects.create(**task_data, user=user)

    # Act
    res = client.get(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()) == 1
    res_dict = res.json()[0]
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    assert str(task.id) == res_dict.pop("id")
    assert str(user.id) == res_dict.pop("user")
    assert res_dict == task_data


@pytest.mark.django_db
def test_get_task(
    client: APIClient, user: UserModel, task_data: dict[str, Any]
) -> None:
    # Arrange
    task = TaskModel.objects.create(**task_data, user=user)
    url = reverse("tasks-detail", args=[task.id])

    # Act
    res = client.get(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_200_OK
    res_dict = res.json()
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    assert str(task.id) == res_dict.pop("id")
    assert str(user.id) == res_dict.pop("user")
    assert res_dict == task_data

    # Arrange
    url = reverse("tasks-detail", args=["id"])

    # Act
    res = client.get(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_task(
    client: APIClient, user: UserModel, task_data: dict[str, Any]
) -> None:
    # Arrange
    task = TaskModel.objects.create(**task_data, user=user)
    url = reverse("tasks-detail", args=[task.id])
    new_title = "New title"
    data = {
        "title": "New title",
    }

    # Act
    res = client.patch(path=url, data=data, format="json")

    # Assert
    assert res.status_code == status.HTTP_200_OK
    res_dict = res.json()
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    assert str(task.id) == res_dict.pop("id")
    assert res_dict.pop("title") == new_title
    assert res_dict.pop("description") == task_data["description"]
    assert res_dict.pop("status") == task_data["status"]

    # Arrange
    new_description = "New description"
    data = {
        "description": new_description,
    }

    # Act
    res = client.patch(path=url, data=data, format="json")

    # Assert
    assert res.status_code == status.HTTP_200_OK
    res_dict = res.json()
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    assert str(task.id) == res_dict.pop("id")
    assert res_dict.pop("description") == new_description
    assert res_dict.pop("title") == new_title
    assert res_dict.pop("status") == task_data["status"]

    # Arrange
    new_status = "done"
    data = {
        "status": new_status,
    }

    # Act
    res = client.patch(path=url, data=data, format="json")

    # Assert
    assert res.status_code == status.HTTP_200_OK
    res_dict = res.json()
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    assert str(task.id) == res_dict.pop("id")
    assert res_dict.pop("description") == new_description
    assert res_dict.pop("title") == new_title
    assert res_dict.pop("status") == new_status

    # Arrange
    url = reverse("tasks-detail", args=["id"])

    # Act
    res = client.get(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_task(
    client: APIClient, user: UserModel, task_data: dict[str, Any]
) -> None:
    # Arrange
    task = TaskModel.objects.create(**task_data, user=user)
    url = reverse("tasks-detail", args=[task.id])

    # Act
    res = client.delete(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_204_NO_CONTENT

    # Arrange
    url = reverse("tasks-detail", args=[task.id])

    # Act
    res = client.delete(path=url, format="json")

    # Assert
    assert res.status_code == status.HTTP_404_NOT_FOUND
