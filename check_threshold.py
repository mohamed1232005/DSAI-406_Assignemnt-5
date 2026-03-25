import sys

THRESHOLD = 0.85

try:
    with open("accuracy.txt", "r") as f:
        accuracy = float(f.read().strip())
except FileNotFoundError:
    print("ERROR: accuracy.txt not found.")
    sys.exit(1)
except ValueError:
    print("ERROR: Invalid accuracy value.")
    sys.exit(1)

print(f"Accuracy: {accuracy}")
print(f"Threshold: {THRESHOLD}")

if accuracy < THRESHOLD:
    print("FAIL ❌")
    sys.exit(1)

print("PASS ✅")