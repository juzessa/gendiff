def space(action, level, base_space=4):
    symbols = {'added': '+ ', 'deleted': '- ',
               'unchanged': '  ', 'nested': ' '}
    space = ' ' * (base_space + level * 2) + symbols[action]
    return space


def if_bool(value, level, base_space=4):
    if isinstance(value, bool):
        r = str(value).lower()
        return r
    elif value is str:
        return f'"{value}"'
    elif value is None:
        return "null"
    elif isinstance(value, dict):
        ans = [
            f"{space('unchanged', level + 1, base_space)}{k}: {if_bool(v, level + 1, base_space)}" for k,
            v in value.items()]
        return "{\n" + "\n".join(ans) + f"\n{' ' * (base_space + level * 2)}}}"
    else:
        return str(value)


def stylish(data, level=0, base_space=4):
    res = []
    for dct in data:
        if dct['action'] == 'added':
            res.append(
                f"{space('added', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'deleted':
            res.append(
                f"{space('deleted', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'unchanged':
            res.append(
                f"{space('unchanged', level, base_space)}{dct['key']}: {if_bool(dct['value'], level, base_space)}")
        elif dct['action'] == 'modified':
            res.append(
                f"{space('deleted', level, base_space)}{dct['key']}: {if_bool(dct['value1'], level, base_space)}")
            res.append(
                f"{space('added', level, base_space)}{dct['key']}: {if_bool(dct['value2'], level, base_space)}")
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
