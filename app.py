import hashlib
import time
import random
import os

from flask import Flask
from flask import request

import conf
from services import rq_queue


app = Flask('servator')


@app.route('/', methods=['GET'])
def index():
	return """
		<form method="POST" action="/upload" enctype="multipart/form-data">
			<input name="serve" type="file">
			<input type="submit">
		</form>
	"""


@app.route('/upload', methods=['POST'])
def upload():
	serve = request.files.get('serve')
	if not serve:
		pass
	mimetype = serve.mimetype
	serve_path = generate_serve_path(serve.filename)
	serve.save(serve_path)


def generate_serve_path(filename):
	serve_code = generate_serve_code(filename)
	serve_directory = os.path.join(conf.SERVE_DIRECTORY_PATH, serve_code)
	while os.path.exists(serve_directory):
		serve_code = generate_serve_code(filename)
		serve_directory = os.path.join(conf.SERVE_DIRECTORY_PATH, serve_code)
	os.mkdir(serve_directory)
	return os.path.join(serve_directory, filename)


def generate_serve_code(filename):
	seed = unicode(time.time()) + unicode(random.randint(0, 9))
	hs = hashlib.md5(filename + seed)
	hx = hs.hexdigest()[:10]
	return hx


if __name__ == '__main__':
	app.run(debug=True)
