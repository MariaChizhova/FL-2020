import argparse
import os
from parser_impl import parse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True, type=str, help='Path to program file')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    with open(args.input, 'r') as input_file:
        tree = parse(input_file.read())
    with open(os.path.basename(args.input) + '.out', 'w') as ans_file:
        ans_file.write(str(tree))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('Error occurred while parsing file: {}'.format(str(e)))
        exit(1)
