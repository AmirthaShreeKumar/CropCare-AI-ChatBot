import io
import os
import re
import tempfile
import time
from pathlib import Path

from PIL import Image


ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png"}
ALLOWED_IMAGE_MIME = {"image/jpeg", "image/png"}
ALLOWED_AUDIO_SIGNATURES = [b"RIFF", b"ID3", b"\xff\xfb", b"\xff\xf3", b"\xff\xf2"]


class UploadValidationError(ValueError):
    pass


def secure_filename(filename: str) -> str:
    filename = os.path.basename(filename or "")
    filename = re.sub(r"[^A-Za-z0-9_.-]", "_", filename)
    return filename[:140] or "upload"


def validate_image_upload(uploaded_file, max_size_mb: int = 6) -> str:
    content = uploaded_file.read()
    if not content:
        raise UploadValidationError("Uploaded image is empty.")

    if len(content) > max_size_mb * 1024 * 1024:
        raise UploadValidationError(
            f"Image file is too large. Maximum allowed size is {max_size_mb} MB."
        )

    ext = Path(uploaded_file.name or "").suffix.lower().lstrip(".")
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise UploadValidationError("Only PNG and JPEG images are allowed.")

    if uploaded_file.type and uploaded_file.type not in ALLOWED_IMAGE_MIME:
        raise UploadValidationError("Only PNG and JPEG images are allowed.")

    try:
        image = Image.open(io.BytesIO(content))
        image.verify()
        format_name = image.format.lower() if image.format else ""
        if format_name not in {"jpeg", "png"}:
            raise UploadValidationError("Uploaded image format is not a valid JPEG or PNG.")
    except UploadValidationError:
        raise
    except Exception as exc:
        raise UploadValidationError("Uploaded image is invalid or corrupted.") from exc

    safe_name = secure_filename(uploaded_file.name)
    suffix = f".{ext}" if ext else ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix, prefix="cropcare_img_") as tmp_file:
        tmp_file.write(content)
        return tmp_file.name


def validate_audio_bytes(audio_bytes: bytes, max_size_mb: int = 10) -> bytes:
    if not audio_bytes:
        raise UploadValidationError("Uploaded audio is empty.")

    if len(audio_bytes) > max_size_mb * 1024 * 1024:
        raise UploadValidationError(
            f"Audio is too large. Maximum allowed size is {max_size_mb} MB."
        )

    if not any(audio_bytes.startswith(signature) for signature in ALLOWED_AUDIO_SIGNATURES):
        raise UploadValidationError("Unsupported audio format. Only WAV and MP3 audio are accepted.")

    return audio_bytes


def cleanup_temp_uploads(prefix: str = "cropcare_img_", max_age_seconds: int = 3600) -> int:
    temp_dir = tempfile.gettempdir()
    removed = 0
    now = time.time()
    for path in Path(temp_dir).glob(f"{prefix}*"):
        try:
            if path.is_file() and (path.stat().st_mtime + max_age_seconds) < now:
                path.unlink(missing_ok=True)
                removed += 1
        except Exception:
            continue
    return removed
