import unittest
from smartfan.app.prediction import predict

class TestAlgorithm(unittest.TestCase):
    def test_offline(self):
        self.assertTrue(predict(65, 75, 80, 72))

    def test_offline2(self):
        self.assertTrue(predict(65, 75, 60, 78))

    def test_offline3(self):
        self.assertFalse(predict(60, 70, 64, 71))

    def test_offline4(self):
        self.assertFalse(predict(60, 70, 58, 55))

    def test_online(self):
        self.assertTrue(predict(65, 75, 74, 60, [61, 64, 69, 72, 76, 80, 81, 81, 82, 83, 81, 80]))

    def test_online2(self):
        self.assertTrue(predict(65, 75, 66, 73, [73, 74, 72, 69, 68, 66, 63, 62, 64, 65, 66, 65]))

    def test_online3(self):
        self.assertFalse(predict(70, 80, 72, 77, [76, 77, 79, 80, 82, 82, 83, 84, 86, 87, 86, 88]))

    def test_online4(self):
        self.assertFalse(predict(70, 80, 79, 74, [74, 74, 72, 71, 69, 69, 68, 66, 65, 67, 67, 66]))