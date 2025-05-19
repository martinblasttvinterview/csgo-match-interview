import pytest
from httpx import AsyncClient

from tests.utils import mock_match_file

URL = "/stats/money-spent-per-round"


mock_file_content = """
11/28/2021 - 20:00:00: MatchStatus: Score: 0:0 on map "de_nuke" RoundsPlayed: 0
11/28/2021 - 20:00:00: MatchStatus: Score: 0:0 on map "de_nuke" RoundsPlayed: 0
11/28/2021 - 20:00:01: "a<5><STEAM_1:1:60631591><CT>" money change 1000-600 = $400 (tracked) (purchase: weapon_incgrenade)
11/28/2021 - 20:00:01: "a<5><STEAM_1:1:60631591><CT>" money change 1000-600 = $400 (tracked) (purchase: weapon_incgrenade)
11/28/2021 - 20:01:00: MatchStatus: Score: 0:1 on map "de_nuke" RoundsPlayed: 1
11/28/2021 - 20:01:00: MatchStatus: Score: 0:1 on map "de_nuke" RoundsPlayed: 1
11/28/2021 - 20:01:01: "a<5><STEAM_1:1:60631591><CT>" money change 1000-600 = $400 (tracked) (purchase: weapon_incgrenade)
11/28/2021 - 20:02:00: MatchStatus: Score: 0:2 on map "de_nuke" RoundsPlayed: 2
11/28/2021 - 20:02:00: MatchStatus: Score: 0:2 on map "de_nuke" RoundsPlayed: 2
11/28/2021 - 20:03:00: MatchStatus: Score: 0:3 on map "de_nuke" RoundsPlayed: 3
11/28/2021 - 20:03:00: MatchStatus: Score: 0:3 on map "de_nuke" RoundsPlayed: 3
11/28/2021 - 20:03:01: "a<5><STEAM_1:1:60631591><CT>" money change 1000-600 = $400 (tracked) (purchase: weapon_incgrenade)
11/28/2021 - 20:04:00: MatchStatus: Score: 0:4 on map "de_nuke" RoundsPlayed: 4
11/28/2021 - 20:04:00: MatchStatus: Score: 0:4 on map "de_nuke" RoundsPlayed: 4
"""


@pytest.mark.anyio
async def test_get_money_spent_per_round(
    client: AsyncClient,
) -> None:
    with mock_match_file(mock_file_content):
        params = {"start": 1, "end": 3}
        response = await client.get(URL, params=params)
        assert response.status_code == 200
        assert response.json()["data"] == {
            "round_with_numeric": [
                {"round_num": 1, "numeric": 1200},
                {"round_num": 2, "numeric": 600},
                {"round_num": 3, "numeric": 0},
            ]
        }
