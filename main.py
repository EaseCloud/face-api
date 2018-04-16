#!/usr/bin/env python3

import imghdr
import json
import os
import pickle
import re
import tempfile
import sys
import traceback

import face_recognition
import numpy
from bottle import route, post, run, request, error, Response

import config


def read_data(group_id):
    """ Read the face encodings of a specific group from the repository.
    :param group_id:
    :return:
    """
    path = os.path.join(config.DIR_DATA, group_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        pickle.dump({}, open(path, 'wb'))
    return pickle.load(open(path, 'rb'))


def write_data(group_id, face_id, face):
    """ Write a face to a group repository.
    :param group_id:
    :param face_id:
    :param face:
    :return:
    """
    data = read_data(group_id)
    data[face_id] = face
    path = os.path.join(config.DIR_DATA, group_id)
    pickle.dump(data, open(path, 'wb'))


def make_response(msg='', ok=True, data=None):
    print('Response {}: {}'.format(msg, 'Success' if ok else 'Fail'), file=sys.stderr)
    payload = dict(ok=ok, msg=msg)
    if data:
        payload['data'] = data
    return Response(
        json.dumps(payload),
        status=200 if ok else 400,
        headers={'Content-Type': 'application/json'},
    )


@error()
def error():
    """ Hides all errors to the client.
    """
    print(traceback.format_exc(), file=sys.stderr)
    return json.dumps(dict(
        ok=False,
        msg='Internal error.',
    ))


@post(os.path.join(r'/', config.PATH, r'upload/<group_id>/<face_id>'))
def upload(group_id, face_id):
    """ Upload a face to a specific group
    :param group_id: Group id, accepts characters from [0-9A-Za-z]
    :param face_id: Face id, accepts characters from [0-9A-Za-z]
    :return:
    """
    # Validate the name
    if not re.match(r'^[0-9A-Za-z]+$', group_id):
        return make_response('Malformed group id.')
    if not re.match(r'^[0-9A-Za-z]+$', face_id):
        return make_response('Malformed face id.')

    # Upload file
    file = request.files.get('file')
    path = os.path.join(config.DIR_UPLOADS, group_id, face_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path, overwrite=True)
    ext = imghdr.what(path)
    os.rename(path, os.path.join(path + '.' + ext))
    path += '.' + ext

    # Parse the faces from the uploaded file
    image = face_recognition.load_image_file(path)
    faces = face_recognition.api.face_encodings(image, num_jitters=config.JITTERS)
    if len(faces) == 0:
        os.remove(path)
        return make_response('No face detected.', False)
    elif len(faces) > 1:
        os.remove(path)
        return make_response('More than one face detected.', False)
    write_data(group_id, face_id, faces[0])

    return make_response('Upload success: group_id={} face_id={}'.format(group_id, face_id))


@post(os.path.join(r'/', config.PATH, r'recognize/<group_id>'))
def recognize(group_id):
    """ Recognize the faces in uploaded picture within the group repository.
    :param group_id: Group id, accepts characters from [0-9A-Za-z]
    :return:
    """
    # Validate the name
    if not re.match(r'^[0-9A-Za-z]+$', group_id):
        return make_response('Malformed group id.')

    # Upload file
    file = request.files.get('file')
    path = os.path.join(config.DIR_UPLOADS, tempfile.mktemp()[1:])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path, overwrite=True)

    # Read faces in repository
    data = read_data(group_id)
    names = list(data.keys())
    faces = numpy.array(list(data.values()))
    # print(names, faces)

    # Parse the faces in the uploaded image
    image = face_recognition.load_image_file(path)
    matches = set()
    upload_faces = face_recognition.api.face_encodings(image, num_jitters=config.JITTERS)
    print('{} faces detected in the picture'.format(len(upload_faces)), file=sys.stderr)
    if len(upload_faces) > 4:
        return make_response('Too many faces in the picture', False)

    # Recognize the faces
    for face in upload_faces:
        results = face_recognition.compare_faces(faces, face, config.TOLERANCE)
        for name, success in zip(names, results):
            if success:
                matches.add(name)

    # Response
    if matches:
        return make_response('Matched {} faces.'.format(len(matches)), data=list(matches))
    else:
        return make_response('No matches.', False)


if __name__ == '__main__':
    run(host='0.0.0.0', port=config.PORT)
