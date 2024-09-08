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


def represent(same, minus, plus):
    res = []
    counter = -1
    operation = ['    ', '  - ', '  + ']
    for lst in [same, minus, plus]:
        counter += 1
        for j in lst:
            j.append(operation[counter])
            res.append(j)
    res = sorted(res, key=lambda x: x[0])
    ans = '{\n'
    for key, value, operation in res:
        if isinstance(value, bool):
            value = ['false', 'true'][value]
        ans += operation + str(key) + ':' + ' ' + str(value) + '\n'
    ans += '}'
    return ans


def find_difference(first_file, second_file):
    set1 = set(read_file(first_file).items())
    set2 = set(read_file(second_file).items())
    same = [list(i) for i in set1.intersection(set2)]
    minus = [list(i) for i in (set1 - set2)]
    plus = [list(i) for i in (set2 - set1)]
    res = represent(same, minus, plus)
    return res

