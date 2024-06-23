import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetOwnedGames(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        STEAM_WEB_API_KEY: str = credentials.credentials.get("STEAM_WEB_API_KEY")
        steamid: int = plugin_input.input_params.get("steamid")

        async with ClientSession() as session:
            get_owned_games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_WEB_API_KEY}&steamid={steamid}&format=json&include_appinfo=true"

            async with session.get(get_owned_games_url, proxy=CONFIG.PROXY) as games_response:
                if games_response.status == 200:
                    games_data = await games_response.json()
                    games = games_data.get("response", {}).get("games", [])
                    game_data = []

                    for game in games:
                        game_data.append(
                            {
                                "game_appid": game.get("appid", ""),
                                "game_name": game.get("name", ""),
                                "img_icon_url": game.get("img_icon_url", ""),
                            }
                        )

                    return PluginOutput(data={"result": json.dumps(game_data)})
                else:
                    games_error_data = await games_response.json()
                    raise_provider_api_error(json.dumps(games_error_data))
