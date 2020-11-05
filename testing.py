import unittest
from diplom import YaDisk


class TestYaDisk(unittest.TestCase):

    def test_create_folder_200(self):
        ya_disk = YaDisk('1', '', [])   # Во второе поле необходимо ввести токен яндекс диска
        response = ya_disk.create_folder()
        self.assertIn(response.status_code, (200, 201))

    def test_create_folder_401(self):
        ya_disk = YaDisk('2', '', [])
        response = ya_disk.create_folder()
        self.assertEqual(response.status_code, 401)

    def test_create_folder_409(self):
        ya_disk = YaDisk('1', '', [])     # Во второе поле необходимо ввести токен яндекс диска
        response = ya_disk.create_folder()
        self.assertEqual(response.status_code, 409)

