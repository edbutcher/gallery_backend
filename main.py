import json
import os
import sqlite3
import mimetypes

from flask import Flask, request, flash, make_response, g
from flask_cors import CORS

from file_domain import File
from settings import SETTINGS

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = SETTINGS.get('UPLOAD_FOLDER', '/tmp')
CORS(app)
DATABASE = SETTINGS.get('DATABASE')

mimetypes.init()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# helper to close
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class FileDAO(object):
    def create(self, file_object):
        # type: (File) -> File

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO files (file_id, file_name, type) VALUES (?, ?, ?)',
                    (file_object.file_id, file_object.file_name, file_object.type))
        conn.commit()
        return file_object

    def get(self, file_id):
        # type: (str) -> File or None

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM files WHERE file_id = ?', (file_id,))
        file_data = cur.fetchone()

        if not file_data:
            return None

        return File(*file_data)

    def get_all(self):
        # type: () -> [File]

        conn = get_db()
        cur = conn.cursor()
        cur.execute('SELECT * FROM files')
        files_data = cur.fetchall()

        if not files_data:
            return []

        return [File(*file_data) for file_data in files_data]

    def delete(self, file_id):
        # type: (str) -> None

        conn = get_db()
        cur = conn.cursor()
        cur.execute('DELETE FROM files WHERE file_id == ?', (file_id,))
        conn.commit()


file_dao = FileDAO()


@app.route('/file_info/<file_id>', methods=['GET'])
def get_file_info(file_id):
    # type: (str) -> {}

    file_obj = file_dao.get(file_id)
    if file_obj:
        return json.dumps(file_obj.serialize())
    return {}


@app.route('/file_info', methods=['GET'])
def get_all_file_info():
    # type: () -> []

    file_objects = file_dao.get_all()
    return json.dumps([file_obj.serialize() for file_obj in file_objects if file_obj])


@app.route('/upload_file', methods=['POST'])
def upload_file():
    # type: () -> {}

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return {}
    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if not file or file.filename == '':
        flash('No selected file')
        return {}

    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

    _, ext = file.filename.rsplit('.')

    file_obj = File(
        file_id=None,
        file_name=file.filename,
        type=mimetypes.types_map['.' + ext]
    )

    file_obj = file_dao.create(file_obj)
    data = file_obj.serialize()
    return json.dumps(data)


@app.route('/file/<file_name>', methods=['GET'])
def serve_files(file_name):
    # type: (str) -> {}

    with open(os.path.join(app.config['UPLOAD_FOLDER'], file_name), 'rb') as fd:
        response = make_response(fd.read())
        _, ext = file_name.rsplit('.')
        response.headers.set('Content-Type', mimetypes.types_map['.' + ext])
        return response



app.run(host='localhost', port=9000)
