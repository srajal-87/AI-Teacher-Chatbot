from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException


class LanguageDetector:
    """Detect the language of input text using the langdetect library."""

    DEFAULT_LANGUAGE = "en"
    SUPPORTED_LANGUAGES = {"en", "hi", "te"}
    MIN_TEXT_LENGTH = 3

    def __init__(self) -> None:
        """Initialize the language detector."""
        pass

    def detect_language(self, text: str) -> str:
        """Detect the language of the given text."""
        if not self._is_valid_text(text):
            return self.DEFAULT_LANGUAGE
        try:
            detected_lang = detect(text.strip())
            return self._validate_language(detected_lang)
        except LangDetectException:
            return self.DEFAULT_LANGUAGE

    def _is_valid_text(self, text: str) -> bool:
        """Check if text is valid for language detection."""
        if not text or not isinstance(text, str):
            return False
        clean_text = text.strip()
        return len(clean_text) >= self.MIN_TEXT_LENGTH

    def _validate_language(self, detected_lang: str) -> str:
        """Validate if detected language is supported."""
        if detected_lang in self.SUPPORTED_LANGUAGES:
            return detected_lang
        return self.DEFAULT_LANGUAGE
