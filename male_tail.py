#!/usr/bin/env python3.10


import argparse
import logging
import os
import sys
from time import sleep


DEFAULT_N_LINES = 10
SLEEP_TIME = 0.01  # seconds
LINE_LENGTH_BYTES = 128


class MaleTail(object):
    """
    Tool like UNIX "tail"
    """

    def __init__(self, args=None):
        self.args = self.get_args(args)
        self.path_to_file = self.args.path
        self.lines_count = int(self.args.n) if self.args.n else DEFAULT_N_LINES
        self.follow = self.args.f
        self.line_length_bytes = LINE_LENGTH_BYTES
        self.file_descriptor = None
        self.result_list = []

        logging.basicConfig(level=logging.INFO)
        self.log = logging.getLogger()

        if not os.path.exists(self.path_to_file):
            self.log.error('File does not exists')
            exit(0)

    @staticmethod
    def get_args(args: list):
        parser = argparse.ArgumentParser(
            description='Like tail but the same.)'
        )
        parser.add_argument('-f', help='follow', action='store_true')
        parser.add_argument('-n', help='lines to read')
        parser.add_argument('--path', help='path to file', required=True)

        return parser.parse_args(args)

    def print_whole_file(self):
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
                    self.print_whole_file()
                    break

            for line in self.file_descriptor:
                self.result_list.append(line.decode())

            if len(self.result_list) > self.lines_count:
                self.result_list = self.result_list[-self.lines_count:]
                break
            else:
                self.line_length_bytes = self.line_length_bytes * 2

        sys.stdout.write(''.join(self.result_list))

    def get_result_list(self):
        return self.result_list

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
    app = MaleTail()
    app.run()
