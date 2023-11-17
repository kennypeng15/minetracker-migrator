import pandas as pd
from datetime import *
import pytz

# read in the existing CSV file
old_csv_name = input("Please input the path to an existing CSV file with minesweeper game data: ")
data = pd.read_csv(old_csv_name)
# print(data)

# begin transforming the old csv file to the DynamoDB format
# rename columns to match Dynamo conventions
data = data.rename(columns={'Game ID': 'game-id', 'Game Timestamp': 'game-timestamp'})
data = data.rename(columns={'Difficulty': 'difficulty', 'Board Solved': 'board-solved'})
data = data.rename(columns={'Time': 'elapsed-time', 'Estimated Time': 'estimated-time'})
data = data.rename(columns={'3BV': 'board-3bv', 'Completed 3BV': 'completed-3bv'})
data = data.rename(columns={'3BV p s': 'game-3bvps', 'Efficiency': 'efficiency'})
data = data.rename(columns={'Total Clicks': 'total-clicks', 'Useful Clicks': 'useful-clicks'})
data = data.rename(columns={'Wasted Clicks': 'wasted-clicks'})
# print(data)

# calculate a solved percentage column, and filter down to only those that are >= 50% solved
data["board-3bv"] = data["board-3bv"].apply(lambda x: float(x))
data["completed-3bv"] = data["completed-3bv"].apply(lambda x: float(x))
data["solve-percentage"] = (data["completed-3bv"] / data["board-3bv"]) * 100.0
data = data[data["solve-percentage"] >= 50.0]
# print(data)

# convert timestamps to timezoned, UTC timestamps
# we'll assume that all games existing in the CSV were played at UTC-7, so we'll
# add 7 hours and convert to UTC
# print(data["game-timestamp"])
data["game-timestamp"] = data["game-timestamp"].apply(lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
data["game-timestamp"] = data["game-timestamp"].apply(lambda x: x + timedelta(hours=7))
data["game-timestamp"] = data["game-timestamp"].apply(lambda x: x.replace(tzinfo=pytz.UTC))
# print(data["game-timestamp"])
# print(data)

# coalesce missing "estimated-time" values to -1.0
# print(data.isnull().values.any())
# print(data["estimated-time"].isnull().values.any())
data["estimated-time"].fillna(-1.0, inplace = True)
# print(data.isnull().values.any())
# print(data["estimated-time"].isnull().values.any())
# print(data)

# convert types to match dynamo
# note: this'll probably be lost on conversion to CSV then re-reading the CSV, but it's fine
data["game-id"] = data["game-id"].apply(lambda x: str(x))
data["game-timestamp"] = data["game-timestamp"].apply(lambda x: str(x))
data["difficulty"] = data["difficulty"].apply(lambda x: str(x))
data["elapsed-time"] = data["elapsed-time"].apply(lambda x: float(x))
data["estimated-time"] = data["estimated-time"].apply(lambda x: float(x))
data["board-solved"] = data["board-solved"].apply(lambda x: bool(x))
data["completed-3bv"] = data["completed-3bv"].apply(lambda x: int(x))
data["board-3bv"] = data["board-3bv"].apply(lambda x: int(x))
data["game-3bvps"] = data["game-3bvps"].apply(lambda x: float(x))
data["useful-clicks"] = data["useful-clicks"].apply(lambda x: int(x))
data["wasted-clicks"] = data["wasted-clicks"].apply(lambda x: int(x))
data["total-clicks"] = data["total-clicks"].apply(lambda x: int(x))
data["efficiency"] = data["efficiency"].apply(lambda x: float(x))
data["solve-percentage"] = data["solve-percentage"].apply(lambda x: float(x))

# reorder dataframe
data = data[["game-id", "game-timestamp", "difficulty", "elapsed-time", "estimated-time", "board-solved", "completed-3bv", "board-3bv", "game-3bvps", "useful-clicks", "wasted-clicks", "total-clicks", "efficiency", "solve-percentage"]]
# print(data)
data.to_csv("transformed_minetracker_data.csv", index=False)
print("Wrote transformed data CSV to transformed_minetracker_data.csv.")