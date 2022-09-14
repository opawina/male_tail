#!/usr/bin/env python3.10


import argparse
import os
import sys
from time import sleep


DEFAULT_N_LINES = 10
SLEEP_TIME = 0.01  # seconds
LINE_LENGTH_BYTES = 128


class MaleTail(object):
    def __init__(self):
        self.args = self.get_args()
        self.path_to_file = self.args.path
        self.lines_count = int(self.args.n) if self.args.n else DEFAULT_N_LINES
        self.follow = self.args.f
        self.line_length_bytes = LINE_LENGTH_BYTES

        if not os.path.exists(self.path_to_file):
            print('File does not exists')
            exit(0)

    @staticmethod
    def get_args():
        parser = argparse.ArgumentParser(description='Like tail but the same.)')
        parser.add_argument('-f', help='follow', action='store_true')
        parser.add_argument('-n', help='lines to read')
        parser.add_argument('--path', help='path to file', required=True)

        return parser.parse_args()

    def read_file_and_output(self):

        # first part. Reading last N lines and stdout.
        while True:
            result_list = []
            file = open(self.path_to_file, mode='rb')

            try:
                file.seek(-self.lines_count * self.line_length_bytes, 2)  # read last n bytes
            except OSError as e:
                if e.strerror == 'Invalid argument':
                    # file is too small to take part
                    file = open(self.path_to_file, mode='rb')
                    sys.stdout.write(
                        ''.join([line.decode() for line in file.readlines()[-self.lines_count:]]))
                    break

            for line in file:
                result_list.append(line.decode())

            if len(result_list) > self.lines_count:
                result_list = result_list[-self.lines_count:]
                break
            else:
                self.line_length_bytes = self.line_length_bytes * 2

        sys.stdout.write(''.join(result_list))

        # second part. Following the file
        while self.follow:
            try:
                sleep(SLEEP_TIME)
                for line in file:
                    sys.stdout.write(line.decode())
            except KeyboardInterrupt:
                exit(0)


if __name__ == '__main__':

    app = MaleTail()
    app.read_file_and_output()
