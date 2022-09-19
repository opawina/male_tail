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
            file.write(f'{i}\n')


@pytest.mark.parametrize(
    ('path_to_file', 'lines_to_read', 'expected'),
    [
        ('log_0_lines.txt', 2, ''),
        ('log_10_lines.txt', 2, '8\n9\n'),
        ('log_10_lines.txt', 20, '0\n1\n2\n3\n4\n5\n6\n7\n8\n9\n')
    ]
)
def test_file(
        path_to_file, lines_to_read, expected, create_empty_log_file,
        create_log_file, capsys
):
    app = MaleTail(path_to_file, lines_to_read, False)
    app.print_last_n_lines()
    assert capsys.readouterr().out == expected
