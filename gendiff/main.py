import json
import yaml
import os.path
from gendiff.styles.stylish_file import return_stylish


def read_file(file):
    file = os.path.abspath(file)
    format = file.split('.')[-1]
    if format == 'json':
        with open(file) as my_file:
            return json.load(my_file)
    elif format == 'yml' or format == 'yaml':
        with open(file) as my_file:
            return yaml.safe_load(my_file)


class Changes:

    @staticmethod
    def added(key, value):
        return {
            'action': 'added',
            'key': key,
            'value': value
        }

    @staticmethod
    def deleted(key, value):
        return {
            'action': 'deleted',
            'key': key,
            'value': value
        }

    @staticmethod
    def nested(key, value1, value2):
        return {
            'action': 'nested',
            'key': key,
            'child': make_difference(value1, value2)
        }

    @staticmethod
    def unchanged(key, value):
        return {
            'action': 'unchanged',
            'key': key,
            'value': value
        }

    @staticmethod
    def modified(key, value1, value2):
        return {
            'action': 'modified',
            'key': key,
            'value1': value1,
            'value2': value2
        }


def make_difference(data1, data2):
    keys = data1.keys() | data2.keys()
    added, deleted = data2.keys() - data1.keys(), data1.keys() - data2.keys()
    res = []

    for k in keys:
        value1 = data1.get(k)
        value2 = data2.get(k)
        if k in added:
            res.append(Changes.added(k, value2))
        elif k in deleted:
            res.append(Changes.deleted(k, value1))
        elif isinstance(value1, dict) and isinstance(value2, dict):
            res.append(Changes.nested(k, value1, value2))
        elif value1 == value2:
            res.append(Changes.unchanged(k, value1))
        elif value1 != value2:
            res.append(Changes.modified(k, value1, value2))

    return sorted(res, key=lambda x: x['key'])


def find_difference(file1, file2, format="stylish"):
    res1 = read_file(file1)
    res2 = read_file(file2)
    res = make_difference(res1, res2)
    formats = {"stylish": return_stylish}
    return formats.get(format, formats['stylish'])(res)
