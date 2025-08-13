import os
from langdetect import detect, detect_langs
from langdetect.lang_detect_exception import LangDetectException
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)


class ResponseGenerator:
    """Generate factually accurate educational responses using the OpenAI API."""

    DEFAULT_MODEL = "gpt-4o-mini"
    MAX_TOKENS = 500
    TEMPERATURE = 0.7
    CONFIDENCE_THRESHOLD = 0.75

    LANGUAGE_MAP = {
        "en": "English",
        "hi": "Hindi",
        "te": "Telugu"
    }

    def __init__(self) -> None:
        """Initialize the response generator with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = OpenAI(api_key=api_key)

    def generate_response(self, question: str, detected_language: str) -> str:
        """Generate educational response for the given question."""
        # Validate and map language name
        language_name = self.LANGUAGE_MAP.get(detected_language, "English")
        prompt = self._create_strict_prompt(question, language_name)

        # First generation attempt
        response_text = self._call_and_extract(prompt)

        # Post-generation verification
        if not self._is_correct_language(response_text, detected_language):
            # Regenerate with explicit enforcement
            strict_prompt = prompt + f"\n\nIMPORTANT: Your answer MUST be entirely in {language_name}."
            response_text = self._call_and_extract(strict_prompt)

        return response_text

    def _create_strict_prompt(self, question: str, language_name: str) -> str:
        """Create a strict, structured prompt for the AI teacher."""
        return (
            f"You are an experienced teacher. You must answer ONLY in {language_name}.\n\n"
            f"Requirements:\n"
            f"1. Always begin your response in {language_name}.\n"
            f"2. Provide a clear definition, detailed explanation, and at least one example.\n"
            f"3. Ensure your answer is scientifically and factually accurate.\n"
            f"4. If unsure, say you do not know, in {language_name}.\n"
            f"5. Avoid unnecessary English words unless they are technical terms without a local equivalent.\n"
            f"6. Never switch languages in your answer.\n\n"
            f"Student's question: {question}"
        )

    def _call_and_extract(self, prompt: str) -> str:
        """Call the OpenAI API and extract the content."""
        try:
            response = self.client.chat.completions.create(
                model=self.DEFAULT_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=self.MAX_TOKENS,
                temperature=self.TEMPERATURE
            )
            return response.choices[0].message.content.strip()
        except Exception:
            return self._get_fallback_response("en")

    def _is_correct_language(self, text: str, expected_code: str) -> bool:
        """Check if the text matches the expected language."""
        try:
            langs = detect_langs(text)
            if not langs:
                return False
            top_lang = langs[0]
            return top_lang.lang == expected_code and top_lang.prob >= self.CONFIDENCE_THRESHOLD
        except LangDetectException:
            return False

    def _get_fallback_response(self, language: str) -> str:
        """Get fallback response when API call fails."""
        fallback_responses = {
            "en": "I apologize, but I'm having trouble processing your question right now. Please try again later.",
            "hi": "क्षमा करें, मुझे आपके प्रश्न को संसाधित करने में समस्या हो रही है। कृपया बाद में पुनः प्रयास करें।",
            "te": "క్షమించండి, మీ ప్రశ్నను ప్రాసెస్ చేయడంలో నాకు సమస్య వస్తోంది. దయచేసి తర్వాత మళ్లీ ప్రయత్నించండి."
        }
        return fallback_responses.get(language, fallback_responses["en"])

