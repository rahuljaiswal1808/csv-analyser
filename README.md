# csv-analyser

A CLI tool to analyse CSV files — list columns, count values by group, and draw ASCII bar charts.

No dependencies required. Uses Python 3 standard library only.

## Requirements

- Python 3.6+

## Usage

### List columns

Print all column names in a CSV file.

```bash
python3 csv_analyser.py columns <file>
```

**Example:**
```bash
python3 csv_analyser.py columns data.csv
```
```
Columns (4):
  1. name
  2. department
  3. city
  4. salary
```

---

### Group-by count

Show how many times each unique value appears in one or more columns, with ASCII bar charts.
Pass multiple column names or use `all` to run across every column.

```bash
python3 csv_analyser.py groupby <file> <column> [column ...]
python3 csv_analyser.py groupby <file> all
```

**Options:**
- `--no-graph` — print plain counts instead of bar charts

**Examples:**
```bash
# Single column
python3 csv_analyser.py groupby data.csv department

# Multiple columns
python3 csv_analyser.py groupby data.csv department city

# All columns
python3 csv_analyser.py groupby data.csv all
```
```
Group-by count: department

  Engineering  ████████████████████████████████████████ 6
  Marketing    █████████████████████████████████ 5
  HR           ███████████████████████████ 4

Group-by count: city

  New York  ████████████████████████████████████████ 7
  London    ███████████████████████ 4
  Paris     ███████████████████████ 4
```

---

### Full analysis

List all columns and show group-by charts in one command.
Accepts multiple column names or `all`.

```bash
python3 csv_analyser.py analyse <file> <column> [column ...]
python3 csv_analyser.py analyse <file> all
```

**Example:**
```bash
python3 csv_analyser.py analyse data.csv department city
```
```
Columns (4):
  1. name
  2. department
  3. city
  4. salary

Group-by count: department

  Engineering  ████████████████████████████████████████ 6
  Marketing    █████████████████████████████████ 5
  HR           ███████████████████████████ 4

Group-by count: city

  New York  ████████████████████████████████████████ 7
  London    ███████████████████████ 4
  Paris     ███████████████████████ 4
```

---

### Fetch

Fetch values from one or more columns, with optional row filtering.
Use `--where col=value` to filter rows. Repeat `--where` to AND multiple conditions.
Supports `=` (equals) and `!=` (not equals). Use `all` to fetch every column.

```bash
python3 csv_analyser.py fetch <file> <column> [column ...] [--where col=value ...]
python3 csv_analyser.py fetch <file> all [--where col=value ...]
```

**Examples:**
```bash
# Fetch name and salary for Engineering staff
python3 csv_analyser.py fetch data.csv name salary --where department=Engineering

# Fetch all columns for rows where city is London
python3 csv_analyser.py fetch data.csv all --where city=London

# Multiple AND conditions
python3 csv_analyser.py fetch data.csv name department --where city!=London --where department!=HR
```
```
  name   salary
  -----  ------
  Alice  95000
  Carol  105000
  Eve    98000
  Henry  88000
  Karen  110000
  Mia    92000

  6 row(s) matched.
```
