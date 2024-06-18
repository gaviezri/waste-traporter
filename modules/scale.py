import json
from threading import Thread
from typing import Any, Generator
from usb.core import find as find_device, Device

from constants import BASE16, CONFIG_PATH, SCALE

def str_to_hex(s):
    return  hex(int(s, BASE16))

class ScaleDriver:
        
    def __init__(self, set_weight):
        with open(CONFIG_PATH) as config:
            ids = json.load(config)[SCALE]

        self._device:(Generator[Device, Any, None] | None) = find_device(idVendor=str_to_hex(ids["VID"]), idProduct=str_to_hex(ids["PID"]))
        if self._device is None:
            raise ValueError("Scale Not Found - please make sure it is connected!")
    
        if self._device.is_kernel_driver_active(0):
            self._device.detach_kernel_driver(0)

        self._device.set_configuration()
        self.set_weight = set_weight

        Thread(target=self.__read_stable_weight_kg, daemon=True).start()

    def __read(self) -> int:
        endpoint = self._device[0][(0, 0)][0]
        data = self._device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        weight = int(str(data[1:6], 'utf-8')) / 1000.0
        return weight
    
    def __read_stable_weight_kg(self):
        stable_count = 0
        last_weight = None
        
        while True:
            weight = self.__read()
            if last_weight is None or weight == last_weight:
                stable_count += 1
            else:
                stable_count = 0
            
            if stable_count >= 10:
                self.set_weight(weight)
                stable_count = 0
            
            last_weight = weight