from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.api.dependencies.user import get_user_by_path


def test_get_user_by_path_returns_service_result(database, user):
    with patch(
        "app.api.dependencies.user.user_service.get_user", return_value=user
    ) as service:
        result = get_user_by_path(database, 1)

    service.assert_called_once_with(database, 1)
    assert result is user


def test_get_user_by_path_raises_404_when_missing(database):
    with patch("app.api.dependencies.user.user_service.get_user", return_value=None):
        with pytest.raises(HTTPException) as error:
            get_user_by_path(database, 9)

    assert error.value.status_code == 404
    assert error.value.detail == "User not found"
