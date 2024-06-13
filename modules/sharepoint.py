from typing import Dict
from constants import USER, PASS, SITE_URL, FOLDER_URL
from office365.sharepoint.client_context import ClientContext
from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.files.file import File

class SharePointDriver:
    def __init__(self, credentials:Dict):
        self.__credentials = UserCredential(credentials[USER], credentials[PASS])
        self.__ctx = None
        
    def __connect(self):
        self.__ctx = ClientContext(SITE_URL).with_credentials(self.__credentials)

    def __delete_if_exists(self, filename):
        try:
            existsing_file = File(self.__ctx, f"{FOLDER_URL}/{filename}")
            existsing_file.delete_object().execute_query()
        except Exception as e:
            print(e)
    
    def upload_file(self, file_path: str, overwrite: bool = False):
        file_name = file_path.split('/')[-1]
        self.__connect()
        
        try:
            if overwrite:
                self.__delete_if_exists(file_name)
            self.__upload_to_sharepoint(file_path, file_name)
            pass
        except Exception as e:
            print(e)

    def __upload_to_sharepoint(self, file_path, file_name):
        target_folder = self.__ctx.web.get_folder_by_server_relative_url(FOLDER_URL)
        with open(file_path, 'rb') as file_content:
            target_folder.upload_file(file_name, file_content.read())
