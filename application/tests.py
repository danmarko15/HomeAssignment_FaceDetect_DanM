import unittest
from application import app
import json


class TestErrorHandling(unittest.TestCase):

    def test_is_url_image_pass_image(self):
        image_url = 'image.jpg'
        result = app.validate_url_is_image(image_url)
        self.assertIsNone(result)

    def test_is_url_image_fail_not_image(self):
        image_url = 'notimage.notimage'
        with self.assertRaises(ValueError):
            app.validate_url_is_image(image_url)

    def test_is_url_live_pass_live(self):
        image_url = 'https://www.deidentification.co/'
        result = app.validate_url_is_live(image_url)
        self.assertIsNone(result)

    def test_is_url_live_fail_not_live(self):
        image_url = 'falseaddress'
        with self.assertRaises(ConnectionError):
            app.validate_url_is_live(image_url)


class TestFaceDetect(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_face_detect(self):
        image_url = "https://webcomicms.net/sites/default/files/clipart/171200/group-people-image-171200-6219897.png"
        expected_result = 11
        result = self.app.get(f'/api/v1.0/facedetect/{image_url}')
        data = json.loads(result.get_data(as_text=True))
        self.assertEqual(data['number of faces detected'], expected_result)


if __name__ == '__main__':
    unittest.main()
