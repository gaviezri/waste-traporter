from typing import Any, Generator
from usb.core import find as find_device, Device
from constants import VENDOR_ID, PRODUCT_ID

class Driver:
        
    def __init__(self):
        self._device:(Generator[Device, Any, None] | None) = find_device(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
        if self._device is None:
            raise ValueError("Scale Not Found - please make sure it is connected!")
    
        if self._device.is_kernel_driver_active(0):
            self._device.detach_kernel_driver(0)

        self._device.set_configuration()

    def __read(self) -> int:
        endpoint = self._device[0][(0, 0)][0]
        data = self._device.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)
        weight = int(str(data[1:6], 'utf-8')) / 1000.0
        return weight
    
    def read_stable_weight_kg(self):
        stable_count = 0
        last_weight = None
        
        while True:
            weight = self.__read()
            if last_weight is None or weight == last_weight:
                stable_count += 1
            else:
                stable_count = 0
            
            if stable_count >= 10:
                return weight
            
            last_weight = weight