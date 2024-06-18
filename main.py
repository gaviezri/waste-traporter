import datetime
from threading import Thread
from constants import CONFIG_PATH
from modules.controller import Controller
from modules.sharepoint import SharePointDriver
from modules.types import WeighingPayload
from modules.ui import UIDriver


if __name__ == "__main__":
    Controller().run()

    


