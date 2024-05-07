import unittest
import asyncio
from smartfan.data.local_weather import Climate, tb_decode

class TestLocalWeather(unittest.TestCase):
    def test_mac_address(self):
        Climate("Indoors", "44:fe:00:00:0e:d5")

    def test_mac_address2(self):
        Climate("Outdoors", "44:8d:00:00:00:23")

    def test_mac_address3(self):
        with self.assertRaises(Exception):
            Climate("Indoors", "51:de:00:0e:00:f1")

    def test_mac_address4(self):
        with self.assertRaises(Exception):
            Climate("Outdoors", "d2:o4:00:0n:33")

    def test_temp(self):
        test = Climate("Indoors", "44:fe:00:00:0e:d5")
        asyncio.run(test.sensorClient())
        self.assertIsInstance(test.getTempF(), float)

    def test_temp(self):
        test = Climate("Outdoors", "d2:o4:00:0n:33")
        asyncio.run(test.sensorClient())
        self.assertIsInstance(test.getTempC(), int)

    def test_tb_decode(self):
        self.assertLessEqual(tb_decode(bytes(7538)), 4096)

    def test_tb_decode2(self):
        self.assertGreaterEqual(tb_decode(bytes(4030)), 0)