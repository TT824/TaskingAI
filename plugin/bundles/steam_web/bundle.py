from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class SteamWeb(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        STEAM_WEB_API_KEY: str = credentials.credentials.get("STEAM_WEB_API_KEY")
        steamid: str = 76561199095387949

        get_owned_games_url = f"https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={STEAM_WEB_API_KEY}&steamid={steamid}&format=json&include_appinfo=true"

        async with ClientSession() as session:
            async with session.get(get_owned_games_url, proxy=CONFIG.PROXY) as games_response:
                if games_response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
