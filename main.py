import streamlit as st

from src.chatbot import TeacherChatbot


class ChatApp:
    """Streamlit web application for the AI Teacher Chatbot."""

    APP_TITLE = "🤖 AI Teacher Chatbot"
    APP_DESCRIPTION = "Ask me anything in English, Hindi, or Telugu - I'll respond like a teacher!"
    SESSION_KEY_MESSAGES = "messages"
    SESSION_KEY_CHATBOT = "chatbot"

    def __init__(self) -> None:
        """Initialize the chat application."""
        self._setup_page_config()
        self._initialize_session_state()

    def run(self) -> None:
        """Run the main chat application."""
        self._display_header()
        self._display_chat_history()
        self._handle_user_input()

    def _setup_page_config(self) -> None:
        """Setup Streamlit page configuration."""
        st.set_page_config(
            page_title=self.APP_TITLE,
            page_icon="🤖",
            layout="centered"
        )

    def _initialize_session_state(self) -> None:
        """Initialize session state variables."""
        if self.SESSION_KEY_MESSAGES not in st.session_state:
            st.session_state[self.SESSION_KEY_MESSAGES] = []
        if self.SESSION_KEY_CHATBOT not in st.session_state:
            try:
                st.session_state[self.SESSION_KEY_CHATBOT] = TeacherChatbot()
            except ValueError as e:
                st.error(f"Error initializing chatbot: {str(e)}")
                st.stop()

    def _display_header(self) -> None:
        """Display application header and description."""
        st.title(self.APP_TITLE)
        st.markdown(self.APP_DESCRIPTION)
        st.markdown("---")

    def _display_chat_history(self) -> None:
        """Display conversation history."""
        for message in st.session_state[self.SESSION_KEY_MESSAGES]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if message["role"] == "assistant" and "language" in message:
                    st.caption(f"Detected language: {self._get_language_name(message['language'])}")

    def _handle_user_input(self) -> None:
        """Handle user input and generate response."""
        user_input = st.chat_input("Ask your question here...")
        if user_input:
            self._add_user_message(user_input)
            self._display_user_message(user_input)
            self._generate_and_display_response(user_input)

    def _add_user_message(self, user_input: str) -> None:
        """Add user message to session state."""
        st.session_state[self.SESSION_KEY_MESSAGES].append({
            "role": "user",
            "content": user_input
        })

    def _display_user_message(self, user_input: str) -> None:
        """Display user message in chat."""
        with st.chat_message("user"):
            st.markdown(user_input)

    def _generate_and_display_response(self, user_input: str) -> None:
        """Generate and display chatbot response."""
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                chatbot_response = st.session_state[self.SESSION_KEY_CHATBOT].get_response(user_input)
            if chatbot_response["success"]:
                self._display_successful_response(chatbot_response)
            else:
                self._display_error_response(chatbot_response)

    def _display_successful_response(self, chatbot_response: dict) -> None:
        """Display successful chatbot response."""
        response_text = chatbot_response["response"]
        detected_language = chatbot_response["detected_language"]
        st.markdown(response_text)
        st.caption(f"Detected language: {self._get_language_name(detected_language)}")
        self._add_assistant_message(response_text, detected_language)

    def _display_error_response(self, chatbot_response: dict) -> None:
        """Display error response."""
        error_message = chatbot_response["error"]
        st.error(error_message)
        self._add_assistant_message(error_message, None)

    def _add_assistant_message(self, content: str, language: str) -> None:
        """Add assistant message to session state."""
        message = {"role": "assistant", "content": content}
        if language:
            message["language"] = language
        st.session_state[self.SESSION_KEY_MESSAGES].append(message)

    def _get_language_name(self, language_code: str) -> str:
        """Get human-readable language name from code."""
        language_names = {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu"
        }
        return language_names.get(language_code, language_code)


def main() -> None:
    """Run the chat application."""
    app = ChatApp()
    app.run()


if __name__ == "__main__":
    main()