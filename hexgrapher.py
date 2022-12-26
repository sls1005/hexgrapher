#!/usr/bin/env python
# -*- coding: ASCII -*-
# Hexgrapher 1.0
# A hex-data visualizer.
# Python 3 is recommended for interpreting.
from sys import stdout, stderr, argv, version_info

usage = '''
usage: hexgrapher.py [options] <data>

options:
    -h, --help                          Show this help message and exit.
    -t <type>, --type <type>            The kind of graph to be generated. Possible values: hashes, table, table-up-to-down, table-left-to-right, where "hashes" (meaning a lot of "#") is the default, and "table" an alias for "table-up-to-down."
    --no-color                          Disable colors.

The first command-line argument not starting with "-" (and not recognized as a graph type) is interpreted as the <data> which must be a hexadecimal number.
If <data> is not given, this program reads stdin.
'''
digits = "0123456789ABCDEF"
colors = dict(zip(digits, (3 * [36, 31, 32, 33, 34, 35])[:16]))
                            # cyan, red, green, yellow, blue, purple
if version_info.major < 3:
    input = raw_input
    range = xrange

def hashes(data, colorful = True):
    if len(data) % 2 == 1:
        data += '0'
    assert len(data) % 2 == 0
    if not colorful:
        print("[{}]".format(
            '#' * (len(data) // 2)
        ))
    else:
        stdout.write('[')
        for i in range(0, len(data), 2):
            stdout.write(
                "\033[38;5;{0}m#".format(
                    str(int(data[i:i+2], 16))
                )
            )
        print("\033[0m]")

def table_up2down(data, colorful = True):
    columns = dict(zip(digits, range(0, 16)))
    if len(data) % 2 == 1:
        data += '#'
    assert len(data) % 2 == 0
    print('')
    if colorful:
        for d in digits:
            stdout.write("\033[1;{0}m{1}".format(colors[d], d))
        print("\033[0m")
    else:
        print(digits)
    for i in range(0, len(data), 2):
        x = data[i]
        y = data[i+1]
        if colorful:
            print("{0}\033[1;{1}m{2}\033[0m".format(
                ' ' * columns[x], colors[x], y
            ))
        else:
            print("{0}{1}".format(' ' * columns[x], y))

def table_left2right(data, colorful = True):
    rows = dict(zip(digits, 16 * ['']))
    if len(data) % 2 == 1:
        data += '#'
    assert len(data) % 2 == 0
    print('')
    for i in range(0, len(data), 2):
        y = data[i]
        x = data[i+1]
        row = rows[y]
        rows[y] = "{0}{1}{2}".format(
            row, (i // 2 - len(row)) * ' ', x
        )
    for d in digits:
        if colorful:
            print("\033[1;{0}m{1}{2}\033[0m".format(colors[d], d, rows[d]))
        else:
            print(d + rows[d])

def print_err(msg):
    stderr.write("\033[1;31m[Error]\033[0m %s\n" % msg)

def main():
    output_type = "hashes"
    data = ''
    colorful = True
    functions = {
        'hashes': hashes,
        'table': table_up2down,
        'table-left-to-right': table_left2right,
        'table-up-to-down': table_up2down
    }
    n = len(argv)
    i = 1
    while i < n:
        a = argv[i]
        if len(a) == 0:
            continue
        elif a[0] == '-':
            if a in ('-h', '--help'):
                print(usage)
                exit()
            elif a in ('-t', '--type'):
                if n > i + 1:
                    output_type = argv[i+1]
                    if output_type not in functions.keys():
                        print_err('Unknown kind: "%s"' % output_type)
                        exit(-2)
                    i += 1
                else:
                    print_err('Expect a kind after "%s"' % a)
                    exit(-1)
            elif a == '--no-color':
                colorful = False
            else:
                print_err('Unknown option: "%s"' % a)
                exit(-3)
        else:
            data = a.upper()
        i += 1 
    if data == '':
        data = (input().split()[0]).upper()
    try:
        int(data, 16)
    except ValueError:
        print_err(data + " is not hexadecimal.")
        exit(-4)
    functions[output_type](data, colorful)

if __name__ == '__main__':
    main()
