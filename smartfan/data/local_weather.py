#credit to iskalchev on Github @ https://github.com/iskalchev/ThermoBeacon for
#bluetooth connecting scanner to ORIA ThermoBeacon

import time
import asyncio
import logging

from bleak import BleakScanner

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)-15s %(name)-8s %(levelname)s: %(message)s",
    )

MSG_ADVERTISE_DATA   = 1
MSG_ADVERTISE_MINMAX = 2

class TBAdvertisingMessage:
    def __init__(self, msg_type, id, bvalue):
#        if id not in [0x10, 0x11, 0x15]:
#            raise ValueError()
        self.id = id
        self.msg_type = msg_type
        self.btn = False if bvalue[1]==0 else True
        self.mac = int.from_bytes(bvalue[2:8],byteorder='little')

class TBAdvMinMax(TBAdvertisingMessage):
    def __init__(self, id, bvalue):
        TBAdvertisingMessage.__init__(self, MSG_ADVERTISE_MINMAX, id, bvalue)
        
        self.max = tb_decode_temperature(bvalue[8:10])
        self.max_t = int.from_bytes(bvalue[10:14],byteorder='little')
        self.min = tb_decode_temperature(bvalue[14:16])
        self.min_t = int.from_bytes(bvalue[16:20],byteorder='little')

class TBAdvData(TBAdvertisingMessage):
    def __init__(self, id, bvalue):
        TBAdvertisingMessage.__init__(self, MSG_ADVERTISE_DATA, id, bvalue)

        self.btr = int.from_bytes(bvalue[8:10],byteorder='little')
        self.btr = self.btr*100/3400
        self.tmp = tb_decode_temperature(bvalue[10:12])
        self.hum = tb_decode_humidity(bvalue[12:14])
        self.upt = int.from_bytes(bvalue[14:18],byteorder='little')

def tb_decode_humidity(b:bytes) -> float:
    result = int.from_bytes(b, byteorder='little')/16.0
    if result>4000:
        result -= 4096
    return result

def tb_decode_temperature(b:bytes) -> float:
    result = int.from_bytes(b, byteorder='little')/16.0
    if result>4000:
        result -= 4096
    return result

class Climate:
    def __init__(self, location, mac_address, curr_time = time.localtime()):
        #initialize attributes
        self.curr_time = curr_time
        self.location = location
        self.current_temp = 0
        self.mac_address = mac_address

        #gather current information for current_temp
        #method self.sensorClient()

    async def sensorClient(self):
        #calling this method scans for thermobeacons
        scanner = BleakScanner(self.detection_callback)
        await scanner.start()
        await asyncio.sleep(5)  #can be modified for amount of time to attempt pulling info
        await scanner.stop()

    def detection_callback(self, device, advertisement_data):
        #calling this method pulls information from scanned devices, should not be called on its own
        #without scanner class
        name = advertisement_data.local_name
        if name is None:
            return
        if name != 'ThermoBeacon':
            return
        msg = advertisement_data.manufacturer_data
        #print(device.rssi)
        for key in msg.keys():
            bvalue = msg[key]
            mac = device.address.lower()
            if str(mac) != self.mac_address:
                return
            if len(bvalue)==18:
                data = TBAdvData(key, bvalue)
                print('[{0}] [{6:02x}] T= {1:5.2f}\xb0C, H = {2:3.2f}%, Button:{4}, Battery : {5:02.0f}%, UpTime = {3:8.0f}s'.\
                      format(mac, data.tmp, data.hum, data.upt, 'On ' if data.btn else 'Off', data.btr, data.id))
                self.current_temp = data.tmp
            else:
                data = TBAdvMinMax(key, bvalue)
                print('[{0}] [{5:02x}] Max={1:5.2f}\xb0C at {2:.0f}s, Min={3:5.2f}\xb0C at {4:.0f}s'.\
                      format(mac, data.max, data.max_t, data.min, data.min_t, data.id))

    def getTempF(self):
        #method to return temperature in Fahrenheit
        return round(self.current_temp * (9/5) + 32, 2) #Celsius to Fahrenheit formula

    def getTempC(self):
        #method to return temperature in Celsius
        return self.current_temp

    def getTime(self):
        #method to return current time
        return self.curr_time

    def getLocal(self):
        #method to return the location of the sensor (indoors or outdoors)
        return self.location

#BT Device 1
#44:fe:00:00:0e:d5: ThermoBeacon
#{'uuids': ['0000fff0-0000-1000-8000-00805f9b34fb'],
#'manufacturer_data':
#{16: b'\x00\x80\xd5\x0e\x00\x00\xfeD\xa2\x0c\xd8\x01\xf1\x00\x0c\n\x00\x00'}}

#BT Device 2
#44:8d:00:00:00:23: ThermoBeacon
#{'uuids': ['0000fff0-0000-1000-8000-00805f9b34fb'],
#'manufacturer_data':
#{16: b'\x00\x80#\x00\x00\x00\x8dDi\x0c\xae\x01\x0f\x01\xd6\t\x00\x00'}}
