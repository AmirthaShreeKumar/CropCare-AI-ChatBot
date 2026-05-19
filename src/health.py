import json
import time
from datetime import datetime
from pathlib import Path

from sqlalchemy import text
from src.config import settings
from src.logger import logger
from db import engine
from src.disease_rag import disease_kb_path, vectordb as disease_vectordb
from src.regional_rag import regional_kb_path, vectordb as regional_vectordb

WEIGHTS_PATH = Path("weights/plant_disease_model.pth")
VECTOR_METADATA_FILENAME = "vector_store_metadata.json"


def check_postgres_connection() -> tuple[bool, str]:
    try:
        with engine.begin() as conn:
            conn.execute(text("SELECT 1"))
        return True, "PostgreSQL connection succeeded"
    except Exception as exc:
        return False, f"PostgreSQL connection failed: {exc}"


def check_vector_store(persist_path: Path, vectordb, label: str) -> tuple[bool, str]:
    if not persist_path.exists():
        return False, f"{label} directory missing: {persist_path}"

    if not persist_path.is_dir():
        return False, f"{label} path is not a directory: {persist_path}"

    persisted_files = list(persist_path.iterdir())
    if not persisted_files:
        return False, f"{label} persistence directory is empty: {persist_path}"

    try:
        start = time.perf_counter()
        results = vectordb.similarity_search("health-check", k=1)
        latency_ms = (time.perf_counter() - start) * 1000
        if not results:
            return False, f"{label} vector store accessible but returned zero chunks"
        return True, (
            f"{label} accessible; retrieval_latency_ms={latency_ms:.1f}; "
            f"retrieved_chunks={len(results)}"
        )
    except Exception as exc:
        return False, f"{label} vector store inaccessible: {exc}"


def check_weights() -> tuple[bool, str]:
    if not WEIGHTS_PATH.exists() or not WEIGHTS_PATH.is_file():
        return False, f"Missing model weights file: {WEIGHTS_PATH}"
    return True, "Model weights are available"


def check_api_keys() -> tuple[bool, str]:
    missing = []
    if not settings.google_api_key:
        missing.append("GOOGLE_API_KEY")
    if not settings.groq_api_key:
        missing.append("GROQ_API_KEY")
    if not settings.app_secret:
        missing.append("APP_SECRET")
    if missing:
        return False, f"Missing required env vars: {', '.join(missing)}"
    return True, "All required API keys are configured"


def write_vector_metadata(
    persist_path: Path,
    source: str,
    knowledge_type: str,
    version: int = 1,
    doc_count: int | None = None,
) -> None:
    try:
        metadata = {
            "source": source,
            "knowledge_type": knowledge_type,
            "version": version,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        if doc_count is not None:
            metadata["doc_count"] = doc_count

        with open(persist_path / VECTOR_METADATA_FILENAME, "w", encoding="utf-8") as metadata_file:
            json.dump(metadata, metadata_file, indent=2)
        logger.info("Wrote vector metadata for %s", persist_path)
    except Exception as exc:
        logger.warning("Unable to write vector metadata for %s: %s", persist_path, exc)


def system_health_status() -> dict:
    checks = []

    postgres_ok, postgres_message = check_postgres_connection()
    checks.append({"name": "postgres", "healthy": postgres_ok, "message": postgres_message})

    disease_ok, disease_message = check_vector_store(Path(disease_kb_path), disease_vectordb, "Disease knowledge base")
    checks.append({"name": "disease_vector_store", "healthy": disease_ok, "message": disease_message})

    regional_ok, regional_message = check_vector_store(Path(regional_kb_path), regional_vectordb, "Regional knowledge base")
    checks.append({"name": "regional_vector_store", "healthy": regional_ok, "message": regional_message})

    weights_ok, weights_message = check_weights()
    checks.append({"name": "model_weights", "healthy": weights_ok, "message": weights_message})

    api_ok, api_message = check_api_keys()
    checks.append({"name": "api_keys", "healthy": api_ok, "message": api_message})

    healthy = all(item["healthy"] for item in checks)
    return {
        "healthy": healthy,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


def log_startup_health() -> None:
    status = system_health_status()
    if status["healthy"]:
        logger.info("Startup health check passed: %s", status)
    else:
        logger.error("Startup health check failed: %s", status)
