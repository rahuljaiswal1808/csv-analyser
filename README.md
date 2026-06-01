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

Show how many times each unique value appears in a column, with an ASCII bar chart.

```bash
python3 csv_analyser.py groupby <file> <column>
```

**Options:**
- `--no-graph` — print plain counts instead of a bar chart

**Example:**
```bash
python3 csv_analyser.py groupby data.csv department
```
```
Group-by count: department

  Engineering  ████████████████████████████████████████ 6
  Marketing    █████████████████████████████████ 5
  HR           ███████████████████████████ 4
```

---

### Full analysis

List all columns and show the group-by bar chart in one command.

```bash
python3 csv_analyser.py analyse <file> <column>
```

**Example:**
```bash
python3 csv_analyser.py analyse data.csv city
```
```
Columns (4):
  1. name
  2. department
  3. city
  4. salary

Group-by count: city

  New York  ████████████████████████████████████████ 7
  London    ███████████████████████ 4
  Paris     ███████████████████████ 4
```
