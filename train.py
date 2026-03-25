"""
train.py  — add this pattern to your existing training script
─────────────────────────────────────────────────────────────
The key requirement from the assignment:
  "If training is successful, create model_info.txt containing the Run ID"
"""

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ── Load data ────────────────────────────────────────────────────────────────
X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ── Train inside an MLflow run ────────────────────────────────────────────────
with mlflow.start_run() as run:

    # Train
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluate
    accuracy = accuracy_score(y_test, model.predict(X_test))

    # Log to MLflow
    mlflow.log_metric("accuracy", accuracy)
    mlflow.sklearn.log_model(model, "model")

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Run ID  : {run.info.run_id}")

    # ── REQUIRED BY ASSIGNMENT ────────────────────────────────────────────────
    # Write the Run ID to model_info.txt so the deploy job can read it
    with open("model_info.txt", "w") as f:
        f.write(run.info.run_id)
    with open("accuracy.txt", "w") as f:
        f.write(str(accuracy))

print("Training complete. Run ID saved to model_info.txt")