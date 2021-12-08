import csv
import json

result = {}

with open("movie_titles.csv", encoding="latin-1") as f:
    for line in csv.reader(f):
        _id, year = line[:2]
        title = ", ".join(line[2:])
        result[_id] = title

print(json.dumps(result))
