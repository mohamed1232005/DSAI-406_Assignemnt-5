# ── Base image ──────────────────────────────────────────────────────────────
FROM python:3.10-slim

# ── Accept the MLflow Run ID as a build argument ─────────────────────────────
ARG RUN_ID

# ── Set environment variables ────────────────────────────────────────────────
ENV MODEL_DIR=/opt/ml/model
ENV RUN_ID=${RUN_ID}

# ── Install dependencies ──────────────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Download the model from MLflow using the Run ID ───────────────────────────
# If you don't have a public MLflow server, we simulate with echo.
# Replace the echo line with the real mlflow command when you have a server:
#   RUN mlflow artifacts download \
#       --artifact-uri runs:/${RUN_ID}/model \
#       --dst-path ${MODEL_DIR}
RUN mkdir -p ${MODEL_DIR} && \
    echo "Simulating model download for Run ID: ${RUN_ID}" && \
    echo "${RUN_ID}" > ${MODEL_DIR}/run_id.txt

# ── Copy application source code ──────────────────────────────────────────────
WORKDIR /app
COPY src/ ./

# ── Default command ───────────────────────────────────────────────────────────
CMD ["python", "app.py"]