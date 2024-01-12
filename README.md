# minetracker-migrator
---

(this README focuses on the migrator project only. for the write-up about MineTracker as a whole, 
see https://kennypeng15.github.io/projects/minetracker/index.html)

## Overview and Design
A python application that migrates existing CSV data about minesweeper games to DynamoDB.

`csv_transformer.py` prompts users to input a path to a CSV file with legacy minesweeper.online game data
(i.e., the old format I used before deciding on an improved one). It transforms the dataset by changing
some column names, calculating any new columns necessary, and filtering out any data rows that
don't contain valuable information (i.e., those with > 50% solve percentage). It outputs a 
transformed CSV file to `transformed_minetracker_data.csv`.

`transformed_data_migrator.py` prompts users to input a path to a transformed CSV file (ideally, 
one created with `csv_transformer.py`).
It then uses `boto3` to send all data in the provided CSV to DynamoDB.

Artifacts included in this project are `dynamo_example_data.png`, which shows the data format Dynamo expects;
`minetracker_data.csv`, the original legacy CSV file;
`transformed_minetracker_data.csv`, the result of running `csv_transformer.py` on `minetracker_data.csv`;
and `transformed_minetracker_data_unfiltered.csv`, the result of running `csv_transformer.py` on `minetracker_data.csv` 
but not filtering out any data rows (included for testing purposes).

As of 11/27/2023 (3:15PM CST), everything in this folder has been published.

## Configuration
A minimal `.env` file is expected.

## Invocation
`python csv_transformer.py` or `transformed_data_migrator.py`, and then follow console prompts and instructions.