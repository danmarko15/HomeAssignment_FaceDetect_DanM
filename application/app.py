import facedetect
import mimetypes
import requests
from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route("/")
def home():
    return "<h1>Please use the API: /api/v1.0/facedetect/<path:image_url> or see README for more details </h1>"


@app.route('/api/v1.0/facedetect/<path:image_url>', methods=['GET'])
def detect_faces(image_url):
    validate_url_is_image(image_url)
    validate_url_is_live(image_url)

    image_request = requests.get(image_url)
    with open("../faces_image_1.png", 'wb') as file:
        file.write(image_request.content)
    number_of_faces = facedetect.detect_faces("../faces_image_1.png")
    return make_response(jsonify({'number of faces detected': number_of_faces}), 200)


def validate_url_is_image(image_url):
    mimetype, encoding = mimetypes.guess_type(image_url)
    if not mimetype or not mimetype.startswith("image"):
        raise ValueError()


def validate_url_is_live(image_url):
    try:
        request_url_head = requests.head(image_url)
        if request_url_head.status_code != requests.codes.ok:
            raise ConnectionError()
    except Exception:
        raise ConnectionError()


@app.errorhandler(ValueError)
def handle_value_error(error):
    return make_response(jsonify({'error': "The url provided is not an image, please provide valid url"}), 400)


@app.errorhandler(ConnectionError)
def handle_connection_error(error):
    return make_response(
        jsonify({'error': "The url provided is either broken or unreachable, please validate url and try again"}), 400)


@app.errorhandler(Exception)
def handle_exception(error):
    return make_response(jsonify({'error': "The server encountered an error and failed to process your request"}), 400)


if __name__ == '__main__':  # to run directly from python
    app.run(host='0.0.0.0', debug=True)
