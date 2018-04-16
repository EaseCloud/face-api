import imghdr
import json
import os
import re
import sys
import tempfile
import traceback

from bottle import post, request, error

import config
import utils


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
        return utils.make_response('Malformed group id.')
    if not re.match(r'^[0-9A-Za-z]+$', face_id):
        return utils.make_response('Malformed face id.')

    # Upload file
    file = request.files.get('file')
    path = os.path.join(config.DIR_UPLOADS, group_id, face_id)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path, overwrite=True)
    ext = imghdr.what(path)
    os.rename(path, os.path.join(path + '.' + ext))
    path += '.' + ext

    resp = utils.upload(group_id, face_id, path)
    os.remove(path)

    return resp


@post(os.path.join(r'/', config.PATH, r'recognize/<group_id>'))
def recognize(group_id):
    """ Recognize the faces in uploaded picture within the group repository.
    If POST[keys] given, split the data with '|' and get the keys.
    Then only the face names in the keys list are considered, the others are ignored.
    Otherwise, every face in the group would be considered.
    :param group_id: Group id, accepts characters from [0-9A-Za-z]
    :return:
    """
    # Validate the name
    if not re.match(r'^[0-9A-Za-z]+$', group_id):
        return utils.make_response('Malformed group id.')

    # Upload file
    file = request.files.get('file')
    path = os.path.join(config.DIR_UPLOADS, tempfile.mktemp()[1:])
    os.makedirs(os.path.dirname(path), exist_ok=True)
    file.save(path, overwrite=True)

    # Read faces in repository
    keys = set(request.POST.get('keys').split('|')) \
        if request.POST.get('keys') else None

    resp = utils.recognize(group_id, path, keys)

    os.remove(path)

    return resp

