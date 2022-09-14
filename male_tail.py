#!/usr/bin/env python3.10


import argparse
import os
import sys
from time import sleep


DEFAULT_N_LINES = 10
SLEEP_TIME = 0.01  # seconds
LINE_LENGTH_BYTES = 128


def get_args():
    parser = argparse.ArgumentParser(description='Like tail but the same.')
    parser.add_argument('-f', help='follow', action='store_true')
    parser.add_argument('-n', help='lines to read')
    parser.add_argument('--path', help='path to file', required=True)

    return parser.parse_args()


def read_file_and_output(path_to_file, lines_count, follow):
    line_length_bytes = LINE_LENGTH_BYTES

    # first part. Reading last N lines and stdout.
    while True:
        result_list = []
        file = open(path_to_file, mode='rb')

        try:
            file.seek(-lines_count * line_length_bytes, 2)  # read last n bytes
        except OSError as e:
            if e.strerror == 'Invalid argument':
                # file is too small to take part
                file = open(path_to_file, mode='rb')
                sys.stdout.write(''.join([line.decode() for line in file.readlines()]))
                break

        for line in file:
            result_list.append(line.decode())

        if len(result_list) > lines_count:
            result_list = result_list[-lines_count:]
            break
        else:
            line_length_bytes = line_length_bytes * 2

    sys.stdout.write(''.join(result_list))

    # second part. Following the file
    while follow:
        try:
            sleep(SLEEP_TIME)
            for line in file:
                sys.stdout.write(line.decode())
        except KeyboardInterrupt:
            exit(0)


def main():
    args = get_args()
    path_to_file = args.path
    lines_count = int(args.n) if args.n else DEFAULT_N_LINES

    if not os.path.exists(path_to_file):
        print('File does not exists')

    read_file_and_output(path_to_file, lines_count, args.f)


if __name__ == '__main__':
    main()
