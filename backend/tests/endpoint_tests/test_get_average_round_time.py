import pytest
from httpx import AsyncClient

from tests.utils import mock_match_file

URL = "/stats/avg-round-time"


mock_file_content = """
11/28/2021 - 20:50:00: World triggered "Round_Start"
11/28/2021 - 20:51:05: World triggered "Round_End"
11/28/2021 - 20:52:00: World triggered "Round_Start"
11/28/2021 - 20:53:30: World triggered "Round_End"
"""


@pytest.mark.anyio
async def test_get_average_round_time(
    client: AsyncClient,
) -> None:
    with mock_match_file(mock_file_content):
        response = await client.get(URL)
        assert response.status_code == 200
        assert response.json()["data"]["average_seconds"] == (65 + 90) // 2


mock_file_content_err = """
11/28/2021 - 20:50:00: World triggered "Round_Start"
11/28/2021 - 20:51:05: World triggered "Round_End"
11/28/2021 - 20:52:00: World triggered "Round_Start"
"""


@pytest.mark.anyio
async def test_get_average_round_time_event_length_mismatch(
    client: AsyncClient,
) -> None:
    with mock_match_file(mock_file_content_err):
        response = await client.get(URL)
        assert response.status_code == 500
