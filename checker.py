import os
import sys
import socket
import argparse
import logging
import glob

from urllib.request import urlopen
from packages import helpers

OPTIONS = {
            "l": "c",
            "m": 10,
            "d": 0,
            "x": 0,
            "c": "",
            "n": 250
            }

def parse_args():
    parser = argparse.ArgumentParser(
                    description = 'Plagiarism Checker.')
    parser.add_argument(
            '-l',
            type=str,
            help='Name of language.'
            ),
    parser.add_argument(
            '-d',
            type=str,
            help='Directory containing files to be checked.'
            )
    parser.add_argument(
            '-u',
            type=int,
            help ='MOSS user id.'
            )
    return parser


def check_path(path):
    return os.path.exists(path)

def verify_args(args):
    if not args.u:
        logging.error('Missing user id(-u)')
        exit()
    elif not args.d:
        logging.error('Input location of dir containing files to be '
                      'checked using (-d)')
        exit()
    elif not args.l:
        logging.error('Language name missing (-l)')
        exit()

def abs_path(path):
    return os.path.abspath(path)

def grab_files(path):
    files = []
    for name in glob.glob(path+'/*'):
        display_name = os.path.basename(name)
        files.append((display_name, name))

    if len(files):
        return files
    else:
        logging.error('No files found in "{}"'.format(path))
        exit()

def upload(link, files):
    index = 0
    for (name, path) in files:
        size = os.path.getsize(path)
        msg = 'file {0} {1} {2} {3}\n'.format(
            index,
            OPTIONS['l'],
            size,
            name
        )
        link.send(msg.encode())
        print('Uploading {} ...'.format(name))
        data = open(path, 'rb').read(size)
        link.send(data)
        index += 1
    print('Upload complete')

def transfer(userid, files, language):
    server = 'moss.stanford.edu'
    port = 7690
    link = socket.socket()
    link.connect((server, port))
    print('Connection open')

    link.send('moss {}\n'.format(userid).encode())
    link.send("directory {}\n".format(OPTIONS['d']).encode())
    link.send("X {}\n".format(OPTIONS['x']).encode())
    link.send("maxmatches {}\n".format(OPTIONS['m']).encode())
    link.send("show {}\n".format(OPTIONS['n']).encode())

    link.send("language {}\n".format(language).encode())

    status = link.recv(1024)

    if status == 'no':
        link.send(b'end\n')
        link.close()
        logging.error("Language not compatible by MOSS")
        exit()

    upload(link, files)

    link.send('query 0 {}\n'.format(OPTIONS['c']).encode())
    status = link.recv(1024)
    link.send(b'end\n')
    print('Closing link')
    link.close()

    return status.decode().replace('\n', '')

def main(userid, path, language):
    files = grab_files(path)
    url = transfer(userid, files, language)
    print(url)

def command_line():
    parser = parse_args()
    args = parser.parse_args()
    if len(sys.argv)==1:
        parser.print_help()
        exit()
    verify_args(args)
    USER_ID = args.u
    LOCATION = abs_path(args.d)
    if not check_path(LOCATION):
        logging.error('Directory "{}" does not exit!'.format(args.d))
        exit()
    LANGUAGE = args.l
    main(USER_ID, LOCATION, LANGUAGE)

if __name__ == '__main__':
    command_line()

