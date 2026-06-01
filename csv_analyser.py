#!/usr/bin/env python3
import csv
import sys
import argparse
from collections import Counter
from itertools import islice


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def cmd_columns(file, _args):
    row = next(read_csv(file), None)
    if row is None:
        print("No data found.")
        return
    columns = list(row.keys())
    print(f"\nColumns ({len(columns)}):")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")


def cmd_groupby(file, args):
    column = args.column
    counts = Counter()
    columns = None

    for row in read_csv(file):
        if columns is None:
            columns = list(row.keys())
            if column not in columns:
                print(f'Error: column "{column}" not found. Available: {", ".join(columns)}', file=sys.stderr)
                sys.exit(1)
        counts[row[column] or '(empty)'] += 1

    if not counts:
        print("No data found.")
        return

    entries = counts.most_common()
    if args.no_graph:
        print(f"\nGroup-by count: {column}\n")
        for label, count in entries:
            print(f"  {label}: {count}")
    else:
        draw_bar_chart(entries, column)


def cmd_analyse(file, args):
    column = args.column
    counts = Counter()
    columns = None

    for row in read_csv(file):
        if columns is None:
            columns = list(row.keys())
            if column not in columns:
                print(f'Error: column "{column}" not found. Available: {", ".join(columns)}', file=sys.stderr)
                sys.exit(1)
        counts[row[column] or '(empty)'] += 1

    if not counts:
        print("No data found.")
        return

    print(f"\nColumns ({len(columns)}):")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")

    draw_bar_chart(counts.most_common(), column)


def draw_bar_chart(entries, column):
    bar_width = 40
    max_count = entries[0][1]
    max_label_len = min(30, max(len(k) for k, _ in entries))

    print(f"\nGroup-by count: {column}\n")
    for label, count in entries:
        bar = '█' * round((count / max_count) * bar_width)
        padded = label[:max_label_len].ljust(max_label_len)
        print(f"  {padded}  {bar} {count}")


def main():
    parser = argparse.ArgumentParser(prog='csv-analyser', description='Analyse CSV data from the command line')
    subparsers = parser.add_subparsers(dest='command', required=True)

    p_columns = subparsers.add_parser('columns', help='List all columns in the CSV file')
    p_columns.add_argument('file', help='Path to the CSV file')

    p_groupby = subparsers.add_parser('groupby', help='Show count of each unique value in a column')
    p_groupby.add_argument('file', help='Path to the CSV file')
    p_groupby.add_argument('column', help='Column name to group by')
    p_groupby.add_argument('--no-graph', action='store_true', help='Print plain counts instead of a bar chart')

    p_analyse = subparsers.add_parser('analyse', help='Full analysis: columns and group-by chart')
    p_analyse.add_argument('file', help='Path to the CSV file')
    p_analyse.add_argument('column', help='Column name to group by')

    args = parser.parse_args()

    dispatch = {'columns': cmd_columns, 'groupby': cmd_groupby, 'analyse': cmd_analyse}
    try:
        dispatch[args.command](args.file, args)
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
