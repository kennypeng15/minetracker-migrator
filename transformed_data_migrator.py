import boto3
import os
from os.path import join, dirname, isfile
import csv
import sys
from decimal import Decimal
from dotenv import load_dotenv
from time import sleep

# TODO:
# load necessary environment variables
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

item_count = 0

# prompt user to input csv, read it in
while(True):
    csv_name = input("Please input the path to a CSV file with transformed minesweeper game data: ")
    if isfile(csv_name):
        break
    else:
        print("Invalid file name, please try again.") 

# iterate throuogh csv and publish to dynamo
with open(csv_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    # display how many rows, and ask for confirmation
    item_count = sum(1 for row in reader)
    confirmation = input("There are " + str(item_count) + " rows in the CSV. Continue? (y/n): ")
    if confirmation.strip().lower() != "y":
        print("Confirmation was not supplied. Terminating.")
        sys.exit(0)
    else:
        print("Confirmation was supplied. Proceeding.")

# connect to boto3
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMO_NAME'])

# actually publish
count_index = 1
with open(csv_name, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # read in as correct types
        game_id = str(row["game-id"])
        game_timestamp = str(row["game-timestamp"])
        difficulty = str(row["difficulty"])
        elapsed_time = Decimal(row["elapsed-time"])
        estimated_time = Decimal(row["estimated-time"])
        board_solved = row["board-solved"].lower() == "true" # DO NOT use bool(row["board-solved"]), non-empty strings are truthy!
        completed_3bv = int(row["completed-3bv"])
        board_3bv = int(row["board-3bv"])
        game_3bvps = Decimal(row["game-3bvps"])
        useful_clicks = int(row["useful-clicks"])
        wasted_clicks = int(row["wasted-clicks"])
        total_clicks = int(row["total-clicks"])
        efficiency = Decimal(row["efficiency"])
        solve_percentage = Decimal(row["solve-percentage"])

        # print(row)
        # print(game_id, game_timestamp, difficulty)
        # print(elapsed_time, estimated_time)
        # print(board_solved)
        # print(completed_3bv, board_3bv, game_3bvps)
        # print(useful_clicks, wasted_clicks, total_clicks)
        # print(efficiency, solve_percentage)
        # print("---")

        # uncomment this out when you actually want to do the migration job!
        '''
        table.put_item(
            Item={
                "game-id": game_id,
                "game-timestamp": game_timestamp,
                "difficulty": difficulty,
                "elapsed-time": elapsed_time,
                "estimated-time": estimated_time,
                "board-solved": board_solved,
                "completed-3bv": completed_3bv,
                "board-3bv": board_3bv,
                "game-3bvps": game_3bvps,
                "useful-clicks": useful_clicks,
                "wasted-clicks": wasted_clicks,
                "total-clicks": total_clicks,
                "efficiency": efficiency,
                "solve-percentage": solve_percentage
            }
        )
        '''
        print("published item " + str(count_index) + " of " + str(item_count))
        count_index += 1
        # sleep just to make sure dynamo doesn't get to the point of request throttling
        # e.g., my table has 20 provisioned RCUs, so 1 (second) / 20 = 0.05 seems to make sense
        sleep(0.05)
