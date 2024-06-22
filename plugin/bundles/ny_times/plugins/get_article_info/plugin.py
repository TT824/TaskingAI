import json

from aiohttp import ClientSession


from bundle_dependency import *
from config import CONFIG


class GetArticleInfo(PluginHandler):
    async def execute(self, credentials: BundleCredentials, plugin_input: PluginInput) -> PluginOutput:
        begin_date: str = plugin_input.input_params.get("begin_date")
        end_date: str = plugin_input.input_params.get("end_date")
        page: int = plugin_input.input_params.get("page")
        q: str = plugin_input.input_params.get("q")
        NY_TIMES_API_KEY: str = credentials.credentials.get("NY_TIMES_API_KEY")
        base_url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?q={q}&api-key={NY_TIMES_API_KEY}"

        if begin_date:
            base_url += f"&begin_date={begin_date}"
        if end_date:
            base_url += f"&end_date={end_date}"
        if page:
            base_url += f"&page={page}"
        async with ClientSession() as session:
            async with session.get(url=base_url, proxy=CONFIG.PROXY) as response:
                if response.status == 200:
                    data = await response.json()
                    articles = data.get("response", {}).get("docs", [])
                    article_info = []
                    for article in articles:
                        article_info.append(
                            {
                                "headline": article.get("headline", {}).get("main", ""),
                                "abstract": article.get("abstract", ""),
                                "url": article.get("web_url", ""),
                                "lead_paragraph": article.get("lead_paragraph", "")
                                # Add more fields as needed
                            }
                        )

                    return PluginOutput(data={"result": json.dumps(article_info)})
                else:
                    data = await response.json()
                    raise_provider_api_error(json.dumps(data))
