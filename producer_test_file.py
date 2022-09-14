import os
from time import sleep
from time import time


def create_testing_log_file():
    start_time = time()

    test_file = 'test.txt'

    try:
        os.remove(test_file)
    except FileNotFoundError:
        pass

    for i in range(1, 500_000):
        with open(test_file, 'a') as file:
            file.write('{}-{}{}'.format(i, str(i)*1000, '\n'))

        # to check real-time reading from file
        print(i)
        sleep(1)

    print(time() - start_time)


if __name__ == '__main__':
    create_testing_log_file()
