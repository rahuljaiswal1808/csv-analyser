#!/usr/bin/env python3
import csv
import sys
import argparse
from collections import Counter


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            yield row


def get_columns(file_path):
    row = next(read_csv(file_path), None)
    return list(row.keys()) if row else []


def resolve_columns(requested, available, file):
    if requested == ['all']:
        return available
    invalid = [c for c in requested if c not in available]
    if invalid:
        print(f'Error: column(s) not found in "{file}": {", ".join(invalid)}', file=sys.stderr)
        print(f'Available: {", ".join(available)}', file=sys.stderr)
        sys.exit(1)
    return requested


def group_by(file_path, columns):
    """Read file once and return a Counter per column."""
    counts = {col: Counter() for col in columns}
    for row in read_csv(file_path):
        for col in columns:
            counts[col][row[col] or '(empty)'] += 1
    return counts


def parse_condition(expr):
    """Parse 'col=value' or 'col!=value' into (col, op, value)."""
    for op in ('!=', '='):
        if op in expr:
            col, _, val = expr.partition(op)
            col, val = col.strip(), val.strip()
            if not col:
                raise ValueError(f'Invalid condition: "{expr}"')
            return col, op, val
    raise ValueError(f'Invalid condition "{expr}". Use col=value or col!=value.')


def matches(row, conditions):
    for col, op, val in conditions:
        cell = row.get(col, '')
        if op == '=' and cell != val:
            return False
        if op == '!=' and cell == val:
            return False
    return True


def cmd_fetch(file, args):
    available = get_columns(file)
    if not available:
        print("No data found.")
        return

    fetch_cols = resolve_columns(args.columns, available, file)

    conditions = []
    for expr in (args.where or []):
        try:
            col, op, val = parse_condition(expr)
        except ValueError as e:
            print(f'Error: {e}', file=sys.stderr)
            sys.exit(1)
        if col not in available:
            print(f'Error: filter column "{col}" not found. Available: {", ".join(available)}', file=sys.stderr)
            sys.exit(1)
        conditions.append((col, op, val))

    results = []
    for row in read_csv(file):
        if matches(row, conditions):
            results.append({col: row[col] for col in fetch_cols})

    if not results:
        print("No matching rows.")
        return

    # Print aligned table
    col_widths = {col: len(col) for col in fetch_cols}
    for row in results:
        for col in fetch_cols:
            col_widths[col] = max(col_widths[col], len(row[col]))

    header = '  '.join(col.ljust(col_widths[col]) for col in fetch_cols)
    separator = '  '.join('-' * col_widths[col] for col in fetch_cols)
    print(f"\n  {header}")
    print(f"  {separator}")
    for row in results:
        print('  ' + '  '.join(row[col].ljust(col_widths[col]) for col in fetch_cols))
    print(f"\n  {len(results)} row(s) matched.")


def draw_bar_chart(entries, column):
    bar_width = 40
    max_count = entries[0][1]
    max_label_len = min(30, max(len(k) for k, _ in entries))

    print(f"\nGroup-by count: {column}\n")
    for label, count in entries:
        bar = '█' * round((count / max_count) * bar_width)
        padded = label[:max_label_len].ljust(max_label_len)
        print(f"  {padded}  {bar} {count}")


def cmd_columns(file, _args):
    columns = get_columns(file)
    if not columns:
        print("No data found.")
        return
    print(f"\nColumns ({len(columns)}):")
    for i, col in enumerate(columns, 1):
        print(f"  {i}. {col}")


def cmd_groupby(file, args):
    available = get_columns(file)
    if not available:
        print("No data found.")
        return

    columns = resolve_columns(args.columns, available, file)
    counts_by_col = group_by(file, columns)

    for col in columns:
        entries = counts_by_col[col].most_common()
        if args.no_graph:
            print(f"\nGroup-by count: {col}\n")
            for label, count in entries:
                print(f"  {label}: {count}")
        else:
            draw_bar_chart(entries, col)


def cmd_analyse(file, args):
    available = get_columns(file)
    if not available:
        print("No data found.")
        return

    print(f"\nColumns ({len(available)}):")
    for i, col in enumerate(available, 1):
        print(f"  {i}. {col}")

    columns = resolve_columns(args.columns, available, file)
    counts_by_col = group_by(file, columns)

    for col in columns:
        draw_bar_chart(counts_by_col[col].most_common(), col)


def main():
    parser = argparse.ArgumentParser(prog='csv-analyser', description='Analyse CSV data from the command line')
    subparsers = parser.add_subparsers(dest='command', required=True)

    p_columns = subparsers.add_parser('columns', help='List all columns in the CSV file')
    p_columns.add_argument('file', help='Path to the CSV file')

    p_groupby = subparsers.add_parser('groupby', help='Show count of each unique value in one or more columns')
    p_groupby.add_argument('file', help='Path to the CSV file')
    p_groupby.add_argument('columns', nargs='+', metavar='column',
                           help='Column name(s) to group by, or "all" for every column')
    p_groupby.add_argument('--no-graph', action='store_true', help='Print plain counts instead of a bar chart')

    p_analyse = subparsers.add_parser('analyse', help='Full analysis: columns list and group-by charts')
    p_analyse.add_argument('file', help='Path to the CSV file')
    p_analyse.add_argument('columns', nargs='+', metavar='column',
                           help='Column name(s) to group by, or "all" for every column')

    p_fetch = subparsers.add_parser('fetch', help='Fetch values from column(s), optionally filtered by conditions')
    p_fetch.add_argument('file', help='Path to the CSV file')
    p_fetch.add_argument('columns', nargs='+', metavar='column',
                         help='Column name(s) to fetch, or "all"')
    p_fetch.add_argument('--where', metavar='col=value', action='append',
                         help='Filter condition (col=value or col!=value). Repeatable for AND logic.')

    args = parser.parse_args()

    dispatch = {'columns': cmd_columns, 'groupby': cmd_groupby, 'analyse': cmd_analyse, 'fetch': cmd_fetch}
    try:
        dispatch[args.command](args.file, args)
    except FileNotFoundError:
        print(f"Error: file '{args.file}' not found.", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
