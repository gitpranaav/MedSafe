# ocr_utils.py — MedSafe AI OCR Utilities
# Handles prescription image preprocessing and text extraction via Tesseract OCR.

import re
import time
import logging
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

logger = logging.getLogger(__name__)

# ── Tesseract Configuration ────────────────────────────────────────────────────
# Update this path to match your Tesseract installation directory.
# Windows default: C:\Program Files\Tesseract-OCR\tesseract.exe
# Linux/macOS:     /usr/bin/tesseract  (usually on PATH, no need to set)
TESSERACT_CMD = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess a PIL image for improved OCR accuracy.
    Steps: convert to grayscale → enhance contrast → sharpen.
    """
    # Convert to grayscale
    image = image.convert("L")

    # Enhance contrast (factor > 1 increases contrast)
    image = ImageEnhance.Contrast(image).enhance(2.0)

    # Enhance sharpness
    image = ImageEnhance.Sharpness(image).enhance(2.0)

    # Apply sharpening filter
    image = image.filter(ImageFilter.SHARPEN)

    return image


def extract_text_from_image(image: Image.Image) -> str:
    """
    Extract text from a PIL Image using Tesseract OCR.

    Args:
        image: A PIL Image object (opened from an uploaded file).

    Returns:
        Cleaned OCR text string, or an error message prefixed with 'OCR Error:'.
    """
    t0 = time.perf_counter()
    try:
        processed = preprocess_image(image)
        # --psm 6: Assume a single uniform block of text
        # --oem 3: Default OCR Engine Mode (LSTM + legacy)
        config = "--psm 6 --oem 3"
        raw_text = pytesseract.image_to_string(processed, config=config)
        result = _clean_ocr_text(raw_text)
        elapsed = time.perf_counter() - t0
        logger.info("OCR extraction completed in %.2fs (%d chars)", elapsed, len(result))
        return result
    except pytesseract.TesseractNotFoundError:
        return (
            "OCR Error: Tesseract not found. "
            f"Please install Tesseract and verify the path: {TESSERACT_CMD}"
        )
    except Exception as exc:
        logger.error("OCR extraction failed: %s", exc)
        return f"OCR Error: {exc}"


def _clean_ocr_text(text: str) -> str:
    """
    Remove common OCR artefacts and normalise whitespace.
    """
    # Collapse runs of blank lines to a single blank line
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Collapse multiple spaces to one
    text = re.sub(r" {2,}", " ", text)

    # Remove isolated pipe / backslash characters (common OCR noise)
    text = re.sub(r"(?<!\w)[|\\]{1,3}(?!\w)", "", text)

    # Strip leading/trailing whitespace
    return text.strip()
