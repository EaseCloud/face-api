import argparse

parser = argparse.ArgumentParser(description='Face Recognition Web Service')

parser.add_argument(dest='command', type=str, nargs='?',
                    default='runserver',
                    help='The command to take, use [upload|recognize|runserver]')
parser.add_argument(dest='group', type=str, nargs='?',
                    default='',
                    help='Specify group name when file path')
parser.add_argument(dest='faces', type=str, nargs='?',
                    default='',
                    help='The face name or keys using in CLI upload/recognize command.')
parser.add_argument('--host',
                    dest='host', default='0.0.0.0', type=str,
                    help='The http binding host.')
parser.add_argument('--port',
                    dest='port', default=3721, type=int,
                    help='The http serving port.')
parser.add_argument('--dir-uploads',
                    dest='dir_uploads', default='uploads', type=str,
                    help='The uploaded file storage directory.')
parser.add_argument('--dir-data',
                    dest='dir_data', default='data', type=str,
                    help='The face pattern data storage directory.')
parser.add_argument('--tolerance',
                    dest='tolerance', default=0.4, type=float,
                    help='How much distance between faces to consider it a match. '
                         'Specify float point value from 0 to 1. '
                         'Lower is more strict. 0.6 is typical best performance.')
parser.add_argument('--jitters',
                    dest='jitters', default=1, type=int,
                    help='How many times to re-sample the face when calculating encoding. '
                         'Higher is more accurate, but slower (i.e. 100 is 100x slower)')
parser.add_argument('--path',
                    dest='path', default='/face', type=str,
                    help='The http api path.')
parser.add_argument('--file',
                    dest='file', type=str,
                    help='The CLI upload image file path.')

args = parser.parse_args()

for k, v in args.__dict__.items():
    print('{}={}'.format(k.upper(), v))

# Redeclare
HOST = args.host
PORT = args.port
PATH = args.path
DIR_UPLOADS = args.dir_uploads
DIR_DATA = args.dir_data
TOLERANCE = args.tolerance
JITTERS = args.jitters
COMMAND = args.command
GROUP = args.group
FACES = args.faces
FILE = args.file
