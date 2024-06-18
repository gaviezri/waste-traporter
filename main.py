import datetime
from threading import Thread
from constants import CONFIG_PATH
from modules.controller import Controller
from modules.sharepoint import SharePointDriver
from modules.types import WeighingPayload
from modules.ui import UIDriver


now = datetime.datetime.now()
begin = now.timestamp()

if __name__ == "__main__":
    class MockController:
        def get_weight(self):
            now = datetime.datetime.now().timestamp()
            if now - begin > 6:
                return 15  # Replace with your actual weight retrieval logic
            else:
                return 0
        def record_weighing(self, payload:WeighingPayload):
            print(payload)

    controller = MockController()
    ui = UIDriver(controller)
    ui.start()
    

    


