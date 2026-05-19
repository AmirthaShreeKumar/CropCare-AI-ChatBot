import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from src.logger import logger
from src.health import write_vector_metadata
from src.regional_rag import initialize_regional_kb, regional_kb_path


def _current_timestamp() -> str:
    return datetime.utcnow().isoformat() + "Z"


def _read_markdown_documents(directory: Path) -> Tuple[List[str], List[Dict[str, str]]]:
    documents: List[str] = []
    metadatas: List[Dict[str, str]] = []
    for pattern in ["*.md", "*.txt"]:
        for source_file in sorted(directory.glob(pattern)):
            try:
                raw_text = source_file.read_text(encoding="utf-8").strip()
                if not raw_text:
                    logger.warning("Skipping empty knowledge file: %s", source_file)
                    continue
                documents.append(raw_text)
                metadatas.append(
                    {
                        "source": source_file.name,
                        "knowledge_type": "regional",
                        "ingestion_timestamp": _current_timestamp(),
                    }
                )
            except Exception as exc:
                logger.warning("Skipping corrupted knowledge file %s: %s", source_file, exc)
    return documents, metadatas


def rebuild_regional_embeddings():
    base_path = Path(regional_kb_path)
    logger.info("Starting regional embeddings rebuild for %s", base_path)

    if base_path.exists():
        logger.info("Removing existing regional vector store contents at %s", base_path)
        shutil.rmtree(base_path, ignore_errors=True)

    base_path.mkdir(parents=True, exist_ok=True)

    documents, metadatas = _read_markdown_documents(base_path)
    if documents:
        logger.info("Found %d source files for regional knowledge indexing", len(documents))
    else:
        logger.info("No markdown source files found in %s; falling back to embedded knowledge payload", base_path)

    initialize_regional_kb(force=True)

    write_vector_metadata(
        base_path,
        source="regional_knowledge_base",
        knowledge_type="regional",
        version=1,
        doc_count=len(documents) if documents else None,
    )

    logger.info("Regional embeddings rebuild complete")


if __name__ == "__main__":
    rebuild_regional_embeddings()
