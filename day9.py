import copy

roll_number = 19

def generate_data():
    users = [
        {"id": 1, "data": {"files": ["a.txt", "b.txt"], "usage": 500}},
        {"id": 2, "data": {"files": ["c.txt"], "usage": 300}}
    ]
    return users

def replicate_data(users):
    assignment = users
    shallow = copy.copy(users)
    deep = copy.deepcopy(users)
    return assignment, shallow, deep

def modify_data(data):
    if roll_number % 2 == 0:
        data[0]["data"]["files"].append("new_file.txt")
    else:
        if len(data[0]["data"]["files"]) > 0:
            data[0]["data"]["files"].pop()

    data[0]["data"]["usage"] = data[0]["data"]["usage"] + 200
    return data

def check_integrity(original, shallow, deep):
    leakage = 0
    safe = 0
    overlap = set()

    for i in range(len(original)):
        if original[i]["data"]["files"] != deep[i]["data"]["files"]:
            leakage += 1
        else:
            safe += 1

    original_files = set()
    shallow_files = set()

    for u in original:
        for f in u["data"]["files"]:
            original_files.add(f)

    for u in shallow:
        for f in u["data"]["files"]:
            shallow_files.add(f)

    overlap = original_files.intersection(shallow_files)

    return leakage, safe, len(overlap)


users = generate_data()

print("BEFORE")
print(users)

assignment, shallow, deep = replicate_data(users)

modify_data(shallow)

print("\nAFTER MODIFICATION")
print("\nOriginal Data")
print(users)

print("\nShallow Copy")
print(shallow)

print("\nDeep Copy")
print(deep)

leakage, safe, overlap = check_integrity(users, shallow, deep)

print("\nIntegrity Report")
print("Data Leakage:", leakage)
print("Safe Copies:", safe)
print("Overlap Count:", overlap)

result = (leakage, safe, overlap)

print("\nTuple Result")
print(result)

if leakage > 0:
    corruption = "Data corruption occurs when shallow copy changes affect original nested data."
else:
    corruption = "No corruption detected."

print("\nData Corruption Definition")
print(corruption)