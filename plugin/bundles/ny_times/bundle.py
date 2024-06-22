from aiohttp import ClientSession

from bundle_dependency import *


class NyTimes(BundleHandler):
    async def verify(self, credentials: BundleCredentials):
        NY_TIMES_API_KEY: str = credentials.credentials.get("NY_TIMES_API_KEY")
        q: str = "nba"

        base_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={q}&api-key={NY_TIMES_API_KEY}"

        async with ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    pass
                else:
                    raise_credentials_validation_error()
