import json

from aiohttp import ClientSession

from bundle_dependency import *
from config import CONFIG


class GetTopStoriesInfo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        section: str = plugin_input.input_params.get("section")
        NY_TIMES_API_KEY: str = credentials.credentials.get("NY_TIMES_API_KEY")
        base_url = f"https://api.nytimes.com/svc/topstories/v2/{section}.json?api-key={NY_TIMES_API_KEY}"

        async with ClientSession() as session:
            async with session.get(base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    stories = data.get("results", [])
                    story_info = []
                    for story in stories:
                        story_info.append(
                            {
                                "title": story.get("title", ""),
                                "abstract": story.get("abstract", ""),
                                "url": story.get("url", ""),
                                "published_date": story.get("published_date", ""),
                                # Add more fields as needed
                            }
                        )

                    return PluginOutput(data={"result": json.dumps(story_info)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
