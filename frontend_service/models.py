import typing
from urllib.parse import quote_plus
import logging
import gspread
from gspread import models as g_models, utils

from oauth2client.service_account import ServiceAccountCredentials

DEFAULT_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive",
]


def build_credential_json(
    project_id: str = None,
    private_key_id: str = None,
    private_key=None,
    client_email=None,
    client_id: str = None,
):

    return {
        "type": "service_account",
        "project_id": project_id,
        "private_key_id": private_key_id,
        "private_key": private_key,
        "client_email": client_email,
        "client_id": client_id,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{quote_plus(client_email.encode('utf-8'))}",
    }


def create_credentials_from_file(client_secret, additional_scopes=None):
    scope = (additional_scopes or []) + DEFAULT_SCOPES
    credentials = ServiceAccountCredentials.from_json_keyfile_name(client_secret, scope)

    gc = gspread.authorize(credentials)
    return gc


def create_credentials(additional_scopes=None, **kwargs):
    scope = (additional_scopes or []) + DEFAULT_SCOPES
    credential_dict = build_credential_json(**kwargs)
    logging.info(credential_dict)
    print(credential_dict)
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(
        credential_dict, scope
    )

    gc = gspread.authorize(credentials)
    return gc


class GoogleSheetInterface:
    def __init__(
        self,
        key_location: str = None,
        project_id: str = None,
        private_key_id: str = None,
        private_key=None,
        client_email=None,
        client_id: str = None,
    ):
        if key_location:
            self.gc = create_credentials(key_location)
        else:
            self.gc = create_credentials(
                project_id=project_id,
                private_key=private_key,
                private_key_id=private_key_id,
                client_email=client_email,
                client_id=client_id,
            )
        self.file = None
        self.data = []

    def sheet_names(self):
        return [x.title for x in self.file.worksheets()]

    def get_sheet_by_name(self, name) -> g_models.Worksheet:
        result = [
            x for x in self.file.worksheets() if name.lower() in x.title.strip().lower()
        ]
        if result:
            return result[0]

    def load_file(self, url: str, sheet_name: str):
        self.file = self.gc.open_by_url(url)
        self.sheet = self.get_sheet_by_name(sheet_name)
        return self

    def get_all_records(self):
        return self.sheet.get_all_records()

    async def bulk_save(
        self, column_id: int = None, http_client_function: typing.Callable = None
    ) -> typing.Dict[str, typing.Any]:
        column_values = self.sheet.col_values(column_id)[1:]
        results = await http_client_function(column_values)
        return {x[0]: x[1] for x in zip(column_values, results)}

    async def get_column_dict(
        self, column_name: str, api_call_class
    ) -> typing.Dict[str, typing.Any]:
        options = {
            "pretext": self.bulk_save(
                column_id=10, http_client_function=api_call_class.save_shared_text
            ),
            "media": self.bulk_save(
                column_id=3, http_client_function=api_call_class.save_media_resource
            ),
            "question": self.bulk_save(
                column_id=11, http_client_function=api_call_class.save_shared_questions
            ),
        }
        return await options[column_name]

