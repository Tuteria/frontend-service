from starlette.config import Config
from starlette.datastructures import Secret, URL

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)
DATABASE_URL = config("DATABASE_URL", cast=URL, default="")
GOOGLE_PROJECT_ID = config('GOOGLE_PROJECT_ID')
GOOGLE_PRIVATE_KEY= config('GOOGLE_PRIVATE_KEY')
GOOGLE_PRIVATE_KEY_ID=config('GOOGLE_PRIVATE_KEY_ID')
GOOGLE_CLIENT_EMAIL=config('GOOGLE_CLIENT_EMAIL')
GOOGLE_CLIENT_ID=config('GOOGLE_CLIENT_ID')