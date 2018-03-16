import os
import sys
import socket
import argparse
import logging
import glob

from packages import helpers




def parse_args():
    parser = argparse.ArgumentParser(
                    description = 'Plagiarism Checker')
    parser.add_argument(
            '-d',
            type=str,
            help='directory containing files to be checked'
            )
    parser.add_argument(
            '-u',
            type=int,
            help ='user id given by moss'
            )
    return parser


def check_path(path):
    return os.path.exists(path)

def verify_args(args):
    if not args.u:
        logging.error('Missing user id(-u)')
        exit()
    if not args.d:
        logging.error('Input location of dir containing files to be '
                      'checked using (-d)')
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

def main(userid, path):
    files = grab_files(path)
    print(files)

def command_line():
    parser = parse_args()
    args = parser.parse_args()
    verify_args(args)
    USER_ID = args.u
    print(USER_ID)
    print(args.d)
    LOCATION = abs_path(args.d)
    if not check_path(LOCATION):
        logging.error('Directory "{}" does not exit!'.format(args.d))
        exit()
    print(LOCATION)
    main(USER_ID, LOCATION)


command_line()

