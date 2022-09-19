#!/usr/bin/env python3.10


import argparse
import logging
import os
import sys
from time import sleep


DEFAULT_N_LINES = 10
SLEEP_TIME = 0.01  # seconds
LINE_LENGTH_BYTES = 128


def get_args():
    parser = argparse.ArgumentParser(
        description='Like tail but the same.)'
    )
    parser.add_argument('--path', help='path to file', required=True)
    parser.add_argument('-n', help='lines to read')
    parser.add_argument('-f', help='follow', action='store_true')

    return parser.parse_args()


class MaleTailArgs(object):
    """
    Data structure class contains required args to MaleTail
    """
    def __init__(self, args: argparse.Namespace):
        self.path_to_file = args.path
        self.lines_count = int(args.n) if args.n else DEFAULT_N_LINES
        self.follow = args.f


class MaleTail(object):
    """
    Tool like UNIX "tail"
    """

    def __init__(self, path_to_file: str, lines_count: int, follow: bool):
        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger()
        self.path_to_file = path_to_file
        self.lines_count = lines_count
        self.follow = follow
        self.line_length_bytes = LINE_LENGTH_BYTES
        if not os.path.exists(self.path_to_file):
            self.log.error('File does not exists')
            exit(0)
        else:
            self.file_descriptor = None
        self.result_list = []

    def _print_whole_file(self):
        self.file_descriptor.seek(0)
        sys.stdout.write(
            ''.join([line.decode() for line in
                     self.file_descriptor.readlines()[-self.lines_count:]]
                    ))

    def print_last_n_lines(self):
        """First part. Reading last N lines and stdout."""

        while True:
            self.result_list = []
            self.file_descriptor = open(self.path_to_file, mode='rb')

            try:
                self.file_descriptor.seek(
                    -self.lines_count * self.line_length_bytes, 2)
            except OSError as e:
                if e.strerror == 'Invalid argument':
                    self.log.debug(
                        'File is too small to seek {} bytes from end'.format(
                            -self.lines_count * self.line_length_bytes))
                    self._print_whole_file()
                    break

            for line in self.file_descriptor:
                self.result_list.append(line.decode())

            if len(self.result_list) > self.lines_count:
                self.result_list = self.result_list[-self.lines_count:]
                break
            else:
                self.line_length_bytes = self.line_length_bytes * 2

        sys.stdout.write(''.join(self.result_list))

    def follow_file(self):
        """Second part. Following the file"""

        while self.follow:
            try:
                sleep(SLEEP_TIME)
                for line in self.file_descriptor:
                    sys.stdout.write(line.decode())
            except KeyboardInterrupt:
                exit(0)

    def run(self):
        self.print_last_n_lines()
        self.follow_file()


if __name__ == '__main__':
    args = MaleTailArgs(get_args())
    app = MaleTail(args.path_to_file, args.lines_count, args.follow)
    app.run()
