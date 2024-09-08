import argparse
from gendiff.main import find_difference


def main():
    parser = argparse.ArgumentParser(
        prog='gendiff',
        description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', help='set format of output')

    args = parser.parse_args()
    print(args.first_file, args.second_file, args.format)
    print(find_difference(args.first_file, args.second_file))


if __name__ == '__main__':
    main()
