#!/usr/bin/env node
import { createReadStream } from 'fs';
import { parse } from 'csv-parse';
import { program } from 'commander';
import chalk from 'chalk';

async function readCSV(filePath) {
  return new Promise((resolve, reject) => {
    const records = [];
    createReadStream(filePath)
      .pipe(parse({ columns: true, skip_empty_lines: true, trim: true }))
      .on('data', (row) => records.push(row))
      .on('end', () => resolve(records))
      .on('error', reject);
  });
}

function listColumns(records) {
  if (records.length === 0) {
    console.log(chalk.yellow('No data found.'));
    return;
  }
  const columns = Object.keys(records[0]);
  console.log(chalk.bold.cyan(`\nColumns (${columns.length}):`));
  columns.forEach((col, i) => console.log(`  ${chalk.green(i + 1 + '.')} ${col}`));
}

function groupByCount(records, column) {
  const counts = {};
  for (const row of records) {
    const val = row[column] ?? '(empty)';
    counts[val] = (counts[val] ?? 0) + 1;
  }
  return Object.entries(counts).sort((a, b) => b[1] - a[1]);
}

function drawBarChart(entries, column) {
  const maxCount = entries[0][1];
  const barWidth = 40;
  const maxLabelLen = Math.min(30, Math.max(...entries.map(([k]) => k.length)));

  console.log(chalk.bold.cyan(`\nGroup-by count: ${column}\n`));
  for (const [label, count] of entries) {
    const bar = '█'.repeat(Math.round((count / maxCount) * barWidth));
    const paddedLabel = label.substring(0, maxLabelLen).padEnd(maxLabelLen);
    console.log(`  ${chalk.yellow(paddedLabel)}  ${chalk.green(bar)} ${chalk.white(count)}`);
  }
}

program
  .name('csv-analyser')
  .description('Analyse CSV data from the command line')
  .version('1.0.0');

program
  .command('columns <file>')
  .description('List all columns in the CSV file')
  .action(async (file) => {
    try {
      const records = await readCSV(file);
      listColumns(records);
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
      process.exit(1);
    }
  });

program
  .command('groupby <file> <column>')
  .description('Show count of each unique value in a column')
  .option('--no-graph', 'Skip the bar chart')
  .action(async (file, column, opts) => {
    try {
      const records = await readCSV(file);
      if (records.length === 0) {
        console.log(chalk.yellow('No data found.'));
        return;
      }
      if (!(column in records[0])) {
        console.error(chalk.red(`Column "${column}" not found. Available: ${Object.keys(records[0]).join(', ')}`));
        process.exit(1);
      }
      const entries = groupByCount(records, column);
      if (opts.graph !== false) {
        drawBarChart(entries, column);
      } else {
        console.log(chalk.bold.cyan(`\nGroup-by count: ${column}\n`));
        for (const [label, count] of entries) {
          console.log(`  ${chalk.yellow(label)}: ${chalk.white(count)}`);
        }
      }
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
      process.exit(1);
    }
  });

program
  .command('analyse <file> <column>')
  .description('Full analysis: columns and group-by chart')
  .action(async (file, column) => {
    try {
      const records = await readCSV(file);
      if (records.length === 0) {
        console.log(chalk.yellow('No data found.'));
        return;
      }
      if (!(column in records[0])) {
        console.error(chalk.red(`Column "${column}" not found. Available: ${Object.keys(records[0]).join(', ')}`));
        process.exit(1);
      }
      listColumns(records);
      const entries = groupByCount(records, column);
      drawBarChart(entries, column);
    } catch (err) {
      console.error(chalk.red(`Error: ${err.message}`));
      process.exit(1);
    }
  });

program.parse();
