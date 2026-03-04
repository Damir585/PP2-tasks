import json

data = {
    "name": "Alex",
    "age": 20,
    "city": "Almaty"
}


json_string = json.dumps(data)
print("JSON string:", json_string)


parsed = json.loads(json_string)
print("Name:", parsed["name"])