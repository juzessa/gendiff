import pytest
import json
import yaml
from contextlib import nullcontext as does_not_raise
from gendiff.main import find_difference, read_file


class TestFindDifference:
    @pytest.mark.parametrize(
        "file1, file2",
        [
            ("tests/fixtures/file1.json", "tests/fixtures/file2.json"),
            ("tests/fixtures/file1.yml", "tests/fixtures/file2.yml"),
        ]
    )
    def test_find_difference(self, file1, file2):
        assert isinstance(find_difference(file1, file2), str)

    @pytest.mark.parametrize("file1, file2, expectation",
                             [("tests/fixtures/file1.json",
                               "tests/fixtures/file.json",
                               pytest.raises(FileNotFoundError)),
                                 ("tests/fixtures/file1.yml",
                                  "tests/fixtures/file2.json",
                                  does_not_raise()),
                                 ("tests/fixtures/file1.yml",
                                  None,
                                  pytest.raises(TypeError)),
                                 ("",
                                  "",
                                  pytest.raises(AttributeError)),
                                 ("tests/fixtures/file_empty1.json",
                                  "tests/fixtures/file_empty2.json",
                                  pytest.raises(json.decoder.JSONDecodeError)),
                                 ("tests/fixtures/file_empty1.yml",
                                  "tests/fixtures/file_empty2.yml",
                                  pytest.raises(AttributeError)),
                                 ("tests/fixtures/file1.csv",
                                  "tests/fixtures/file.csv",
                                  pytest.raises(AttributeError)),
                              ])
    def test_find_difference_error(self, file1, file2, expectation):
        with expectation:
            assert find_difference(file1, file2)


class TestReadFile:

    @pytest.mark.parametrize(
        "file",
        [
            ("tests/fixtures/file1.json"),
            ("tests/fixtures/file3.json"),
        ]
    )
    def test_read_file_json(self, file):
        with open(file) as my_file:
            file_text = json.load(my_file)
        res = read_file(file)
        assert res == file_text
    
    @pytest.mark.parametrize(
        "file",
        [
            ("tests/fixtures/file1.yml"),
            ("tests/fixtures/file2.yml"),
        ]
    )
    def test_read_file_json(self, file):
        with open(file) as my_file:
            file_text = yaml.safe_load(my_file)
        res = read_file(file)
        assert res == file_text
