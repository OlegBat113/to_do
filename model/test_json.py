import json

with open("data.json", mode="r", encoding="utf-8") as read_file:
    data = json.load(read_file)

type(data)

print(data)

print(data['user'])

