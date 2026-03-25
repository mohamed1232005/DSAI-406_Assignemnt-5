"""
check_threshold.py
──────────────────
Reads the MLflow Run ID from model_info.txt,
fetches the logged accuracy from the MLflow Tracking Server,
and exits with code 1 (failing the pipeline) if accuracy < 0.85.
"""

import sys
import mlflow

THRESHOLD = 0.85

# ── 1. Read the Run ID ──────────────────────────────────────────────────────
try:
    with open("model_info.txt", "r") as f:
        run_id = f.read().strip()
except FileNotFoundError:
    print("ERROR: model_info.txt not found.")
    sys.exit(1)

if not run_id:
    print("ERROR: model_info.txt is empty.")
    sys.exit(1)

print(f"Checking Run ID: {run_id}")

# ── 2. Connect to MLflow and fetch the run ──────────────────────────────────
client = mlflow.tracking.MlflowClient()

try:
    run = client.get_run(run_id)
except Exception as e:
    print(f"ERROR: Could not fetch run from MLflow: {e}")
    sys.exit(1)

# ── 3. Read the accuracy metric ─────────────────────────────────────────────
accuracy = run.data.metrics.get("accuracy")

if accuracy is None:
    print("ERROR: No 'accuracy' metric found in this run.")
    sys.exit(1)

print(f"Accuracy from MLflow: {accuracy:.4f}")
print(f"Threshold            : {THRESHOLD}")

# ── 4. Pass or fail ─────────────────────────────────────────────────────────
if accuracy < THRESHOLD:
    print(f"FAIL — accuracy {accuracy:.4f} is below threshold {THRESHOLD}. Pipeline stopped.")
    sys.exit(1)   # non-zero exit → GitHub Actions marks step as failed

print(f"PASS — accuracy {accuracy:.4f} meets the threshold. Proceeding to Docker build.")
sys.exit(0)