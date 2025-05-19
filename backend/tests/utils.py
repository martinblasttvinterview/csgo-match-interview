from collections.abc import Generator
from contextlib import contextmanager
from typing import Any
from unittest.mock import mock_open, patch


@contextmanager
def mock_match_file(mock_file_content: str) -> Generator[Any, None, Any]:
    m = mock_open(read_data=mock_file_content)
    with (
        patch("pathlib.Path.open", m),
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.is_file", return_value=True),
    ):
        yield
