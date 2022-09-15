import pytest

from male_tail import MaleTail


# TODO delete files after test


@pytest.fixture()
def create_empty_log_file():
    file_name = 'log_0_lines.txt'
    with open(file_name, 'w') as file:
        pass


@pytest.fixture()
def create_log_file():
    file_name = 'log_10_lines.txt'
    with open(file_name, 'w') as file:
        for i in range(0, 10):
            file.write(f'{i}-{i}\n')


@pytest.mark.parametrize(
    ('args', 'expected'),
    [
        (
                ('--path', 'log_0_lines.txt', '-n', '2'), ''
        ),
        (
                ('--path', 'log_0_lines.txt', '-n', '10'), ''
        ),
        (
                ('--path', 'log_10_lines.txt', '-n', '2'),
                '8-8\n9-9\n'
        ),
        (
                ('--path', 'log_10_lines.txt', '-n', '20'),
                '0-0\n1-1\n2-2\n3-3\n4-4\n5-5\n6-6\n7-7\n8-8\n9-9\n'
        )
    ]
)
def test_file(args, expected, create_empty_log_file, create_log_file, capsys):
    app = MaleTail(args)
    app.print_last_n_lines()
    assert capsys.readouterr().out == expected
