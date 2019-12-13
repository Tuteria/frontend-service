import json
import typing
import os
import aiofiles
import jwt

from frontend_service import models, settings, types

config = dict(
    project_id=settings.GOOGLE_PROJECT_ID,
    private_key=settings.GOOGLE_PRIVATE_KEY,
    private_key_id=settings.GOOGLE_PRIVATE_KEY_ID,
    client_email=settings.GOOGLE_CLIENT_EMAIL,
    client_id=settings.GOOGLE_CLIENT_ID,
)
current_path = os.path.dirname(os.path.abspath(__name__))
JSON_PATH = os.path.join(current_path, "data.json")


async def fetch_regions(
    country: str, model_instance: bool = False, validate_config: bool = False
) -> typing.Union[types.SampleResult, models.GoogleSheetInterface]:
    new_config = {**config}
    if not settings.DEBUG:
        key = new_config["private_key"]
        new_config["private_key"] = json.loads(f'"{key}"')
    if validate_config:
        return types.SampleResult(data=new_config)
    url = "https://docs.google.com/spreadsheets/d/1O0XIhXRvhgJLSyFwlBHaB1ApYTnosRxZM559zNLRdZA/edit?usp=sharing"
    instance = models.GoogleSheetInterface(**new_config)
    instance.load_file(url, "Regions")
    filter_countries = [
        x for x in instance.get_all_records() if x["Country"].lower() == country.lower()
    ]
    result = [{"state": x["State"], "vicinity": x["Region"]} for x in filter_countries]
    if model_instance:
        return instance
    return types.SampleResult(data=result)


async def tutor_search(search_token, page=1) -> types.SampleResult:
    defaultPage = int(page)
    try:
        request_data = jwt.decode(search_token, verify=False)
    except jwt.DecodeError:
        return types.SampleResult(errors={"msg": "Invalid payload"})
    else:
        async with aiofiles.open(JSON_PATH) as f:
            content = await f.read()
            data = json.loads(content)
            result = data["data"][defaultPage - 1]
        return types.SampleResult(data=result)

