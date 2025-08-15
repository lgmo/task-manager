import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from http.cookies import SimpleCookie
from typing import Any

import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.test import APIClient
from rest_framework.views import APIView

from accounts.models import UserModel, UserSessionModel
from tasks.models import TaskModel


def get_authenticate_mock(
    user: UserModel,
) -> Callable[[BasePermission, Request, APIView], bool]:
    def authenticate(
        self: BasePermission,
        request: Request,
    ) -> bool:
        return user, None

    return authenticate


# TODO: uncomment after implementing auth flows
@pytest.mark.django_db
def test_create_task(
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "common.authentications.IsAuthenticated.authenticate",
        get_authenticate_mock(user),
    )
    url = reverse("tasks-list")

    # Act
    res = client.post(path=url, data=task_data, format="json")

    # Assert
    assert res.status_code == status.HTTP_201_CREATED
    res_dict = res.json()
    task = TaskModel.objects.first()
    assert task is not None
    diff = datetime.fromisoformat(res_dict.pop("created_at")) - task.created_at  # noqa: E501
    assert timedelta(minutes=-1) < diff < timedelta(minutes=1)
    diff = datetime.fromisoformat(res_dict.pop("updated_at")) - task.updated_at  # noqa: E501
    assert str(task.id) == res_dict.pop("id")
    assert res_dict == {**task_data, "user": str(user.id)}


@pytest.mark.django_db
def test_create_task_unauthorized(
    client: APIClient,
    task_data: dict[str, Any],
) -> None:
    # Arrange
    url = reverse("tasks-list")

    # Act
    res = client.post(path=url, data=task_data, format="json")

    # Assert
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task_unauthorized_invalid_token(
    client: APIClient,
    task_data: dict[str, Any],
) -> None:
    # Arrange
    url = reverse("tasks-list")
    client.cookies = SimpleCookie({"session_id": "invalid_token"})

    # Act
    res = client.post(path=url, data=task_data, format="json")

    # Assert
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_create_task_unauthorized_user_not_found(
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    url = reverse("tasks-list")
    session = UserSessionModel.objects.create(
        user=user,
        access_token="valid_token",  # noqa: S106
        refresh_token="valid_refresh_token",  # noqa: S106
        expires_at=datetime.now(UTC) + timedelta(hours=1),
    )
    monkeypatch.setattr(
        "common.authentications.auth_service.decode_token",
        lambda token: {"sub": str(uuid.uuid4())},
    )
    client.cookies = SimpleCookie({"session_id": session.id})

    # Act
    res = client.post(path=url, data=task_data, format="json")

    # Assert
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_list_tasks(
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "common.authentications.IsAuthenticated.authenticate",
        get_authenticate_mock(user),
    )
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
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "common.authentications.IsAuthenticated.authenticate",
        get_authenticate_mock(user),
    )
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
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "common.authentications.IsAuthenticated.authenticate",
        get_authenticate_mock(user),
    )
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
    client: APIClient,
    user: UserModel,
    task_data: dict[str, Any],
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    # Arrange
    monkeypatch.setattr(
        "common.authentications.IsAuthenticated.authenticate",
        get_authenticate_mock(user),
    )
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
