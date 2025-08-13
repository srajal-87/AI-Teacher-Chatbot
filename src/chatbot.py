from src.language_detector import LanguageDetector
from src.response_generator import ResponseGenerator


class TeacherChatbot:
    """Coordinate language detection and response generation for the teacher chatbot."""

    def __init__(self) -> None:
        """Initialize the teacher chatbot with required components."""
        self.language_detector = LanguageDetector()
        self.response_generator = ResponseGenerator()

    def get_response(self, user_input: str) -> dict:
        """Process user input and generate teacher response."""
        if not self._is_valid_input(user_input):
            return self._create_error_response("Please provide a valid question.")
        detected_language = self.language_detector.detect_language(user_input)
        response = self.response_generator.generate_response(user_input, detected_language)
        return self._create_success_response(user_input, detected_language, response)

    def _is_valid_input(self, user_input: str) -> bool:
        """Validate user input."""
        return bool(user_input and isinstance(user_input, str) and user_input.strip())

    def _create_error_response(self, error_message: str) -> dict:
        """Create error response dictionary."""
        return {
            "success": False,
            "error": error_message,
            "response": None,
            "detected_language": None,
            "user_input": None
        }

    def _create_success_response(self, user_input: str, detected_language: str, response: str) -> dict:
        """Create success response dictionary."""
        return {
            "success": True,
            "error": None,
            "response": response,
            "detected_language": detected_language,
            "user_input": user_input
        }