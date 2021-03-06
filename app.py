# coding: utf-8

from __future__ import unicode_literals

import zipfile
import hashlib
import time
import random
import os

from flask.views import MethodView
from flask import Flask
from flask import request, redirect, jsonify
from flask.templating import render_template
from werkzeug.exceptions import BadRequest, UnsupportedMediaType

import conf

app = Flask('servator')


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


class UploadHandlerBase(MethodView):

    def post(self):
        serve = request.files.get('serve')
        if not serve:
            raise BadRequest()
        mimetype = serve.mimetype
        if mimetype == 'application/zip':
            serve_code = self.handle_zip(serve)
        elif mimetype == 'text/html':
            serve_code = self.handle_html(serve)
        else:
            raise UnsupportedMediaType(mimetype)
        return self.get_response(serve_code)

    def get_response(self, serve_code):
        raise NotImplementedError

    def handle_zip(self, serve):
        serve_directory, serve_code = get_serve_directory(serve.filename, create=False)
        with zipfile.ZipFile(serve) as zp:
            zp.extractall(serve_directory)
        return serve_code

    def handle_html(self, serve):
        serve_directory, serve_code = get_serve_directory(serve.filename)
        serve.save(os.path.join(serve_directory, serve.filename))
        return serve_code


class WebUploadHandler(UploadHandlerBase):

    def get_response(self, serve_code):
        serve_url = get_serve_url(serve_code)
        return redirect(serve_url)
app.add_url_rule('/upload', view_func=WebUploadHandler.as_view(b'upload'))


class ApiUploadHandler(UploadHandlerBase):

    def get_response(self, serve_code):
        serve_url = get_serve_url(serve_code)
        return jsonify(dict(result=dict(serve_url=serve_url)))
app.add_url_rule('/api/upload', view_func=ApiUploadHandler.as_view(b'api_upload'))


def get_serve_url(serve_code):
    return 'http://%s%s' % (serve_code, conf.SERVATOR_DOMAIN)


def get_serve_directory(filename, create=True):
    serve_code = generate_serve_code(filename)
    serve_directory = os.path.join(conf.SERVE_DIRECTORY_PATH, serve_code)
    if os.path.exists(serve_directory):
        serve_directory = get_serve_directory(filename)
    if create:
        os.makedirs(serve_directory)
    return serve_directory, serve_code


def generate_serve_code(filename):
    seed = unicode(time.time()) + unicode(random.randint(0, 9))
    hs = hashlib.md5(filename + seed)
    hx = hs.hexdigest()[:10]
    return hx


if __name__ == '__main__':
    app.run(debug=False)
