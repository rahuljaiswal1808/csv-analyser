# csv-analyser

A CLI tool to analyse CSV files — list columns, count values by group, and draw ASCII bar charts.

## Installation

```bash
npm install
```

## Usage

### List columns

Print all column names in a CSV file.

```bash
node index.js columns <file>
```

**Example:**
```bash
node index.js columns data.csv
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
node index.js groupby <file> <column>
```

**Options:**
- `--no-graph` — print plain counts instead of a bar chart

**Example:**
```bash
node index.js groupby data.csv department
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
node index.js analyse <file> <column>
```

**Example:**
```bash
node index.js analyse data.csv city
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
