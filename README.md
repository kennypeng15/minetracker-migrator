# minetracker-migrator
Python application that migrates existing CSV data about minesweeper games to DynamoDB.

# Notes:
The CSV structure is:
```
Game ID
Game Timestamp
Difficulty
Board Solved
Time
Estimated Time
3BV
Completed 3BV
3BV p s
Efficiency
Total Clicks
Useful Clicks
Wasted Clicks

e.g.,
2358451094,2023-06-15 23:30:01,expert,False,20.503,79.338,178,46,2.2436,81.0,57,55,2
2358358736,2023-06-15 22:52:19,expert,True,87.824,,166,166,1.8901,67.0,246,218,28
```

---

The DynamoDB structure is:
```
Item={
            "game-id": game_id,
            "game-timestamp": game_timestamp,
            "difficulty": difficulty,
            "elapsed-time": Decimal(str(statistics["elapsed-time"])),
            "estimated-time": Decimal(str(statistics["estimated-time"])),
            "board-solved": statistics["board-solved"],
            "completed-3bv": statistics["completed-3bv"],
            "board-3bv": statistics["board-3bv"],
            "game-3bvps": Decimal(str(statistics["game-3bvps"])),
            "useful-clicks": statistics["useful-clicks"],
            "wasted-clicks": statistics["wasted-clicks"],
            "total-clicks": statistics["total-clicks"],
            "efficiency": Decimal(str(statistics["efficiency"])),
            "solve-percentage": Decimal(str(statistics["solve-percentage"]))
        }

(see screenshot for example)
```

We also need to be mindful of the fact that the timestamps in the CSV are local timestamps (safe to say UTC - 7) without a timezone string, while the DynamoDB entries that exist are all UTC (with an indicative timezone string). We should convert local timezones to UTC.

There are some other small differences to note as well:
- the timestamp
- note that Dynamo has `-1` as the estimated time value if the board is solved, but the CSV just leaves that entry empty - go with Dynamo convention
- CSV doesn't have solved percentage - need to calculate that
- Dynamo only cares about entries where solved percentage >= 20.0

May be best to output filtered, transformed version of old CSV data to another CSV, then read through that and publish to Dynamo.