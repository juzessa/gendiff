import json
import yaml
import os.path

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

    def added(key, value):
        return {
            'action': 'added',
            'key': key,
            'value': value
        }


    def deleted(key, value):
        return {
            'action': 'deleted',
            'key': key,
            'value': value
        }


    def nested(key, value1, value2):
        return {
            'action': 'nested',
            'key': key,
            'child': make_difference(value1, value2)
        }

    def unchanged(key, value):
        return {
            'action': 'unchanged',
            'key': key,
            'value': value
        }


    def modified(key, value1, value2):
        return {
            'action': 'modified',
            'key': key,
            'value1': value2,
            'value2': value1
        }


def make_difference(data1, data2):
    keys = data1.keys() | data2.keys()
    added, deleted = data2.keys() - data1.keys(), data1.keys() - data2.keys()
    res = []

    for k in keys:
        value1 = data1.get(k)
        value2 = data2.get(k)
        if k in added:
            res.append(Changes.added(k, value1))
        elif k in deleted:
            res.append(Changes.deleted(k, value1))
        elif isinstance(value1, dict) and isinstance(value2, dict):
            res.append(Changes.nested(k, value1, value2))
        elif value1 == value2:
            res.append(Changes.unchanged(k, value1))
        elif value1 != value2:
            res.append(Changes.modified(k, value1, value2))

    return sorted(res, key=lambda x: x['key'])


def space(action, level, base_space=4):
    symbols = {'added': '+ ', 'deleted': '- ',
               'unchanged': '  ', 'nested': ' '}
    space = ' ' * (base_space + level * 2) + symbols[action]
    return space

def if_bool(value, level, base_space=4):
    if type(value) is bool:
        r = str(value).lower()
        return r
    elif value is str:
        return f'"{value}"'
    elif value is None:
        return "null"
    elif type(value) is dict:
        ans = [f"{space('unchanged', level + 1, base_space)}{k}: {if_bool(v, level + 1, base_space)}" for k, v in value.items()]
        return "{\n" + "\n".join(ans) + f"\n{' ' * (base_space + level * 2)}}}"
    else:
        return str(value)

def stylish(data, level=0, base_space=4):
    res = []
    for dct in data:
        if dct['action'] == 'added':
            res.append(f"{space('added', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'deleted':
            res.append(f"{space('deleted', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'unchanged':
            res.append(f"{space('unchanged', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'modified':
            res.append(f"{space('deleted', level, base_space)}{dct['key']}: {if_bool(dct['value1'], level, base_space)}")
            res.append(f"{space('added', level, base_space)}{dct['key']}: {if_bool(dct['value2'], level, base_space)}")
        elif dct['action'] == 'nested':
            res.append(f"{space('nested', level, base_space)}{dct['key']}: {{")
            res.extend(stylish(dct['child'], level + 1, base_space))
            res.append(f"{' ' * (base_space + level * 2)}}}")

    return res


def result_stylish(data):
    res = stylish(data)
    print("{")
    for r in res:
        print(r)
    print("}")


def find_difference(file1, file2, format='stylish'):
    res1 = read_file(file1)
    res2 = read_file(file2)
    result_stylish(make_difference(res1, res2))

file1 = '/Users/juliasamsonova/Dev/gendiff/tests/fixtures/file3.json'
file2 = '/Users/juliasamsonova/Dev/gendiff/tests/fixtures/file4.json'
find_difference(file1, file2)