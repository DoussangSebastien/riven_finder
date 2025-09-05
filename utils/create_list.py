import sys

file_path = sys.argv[1]

result = {}

with open(file_path, "r", encoding="utf-8") as f:
    for raw_line in f:
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("#"):
            continue  
        else:
            result[line] = line.lower().replace(" ", "_")

print("riven_attributes = {")
for k, v in result.items():
    print(f'  "{k}": "{v}",')
print("}")
