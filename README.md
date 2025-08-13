# 🤖 AI Teacher Chatbot

An AI-powered teacher chatbot that detects the language of a question (**English**, **Hindi**, **Telugu**) and generates **educational responses** using the OpenAI API.

---

## 🚀 Features

- Automatic language detection (English, Hindi, Telugu)
- Teacher-style educational explanations
- Responds in the same language as input
- Streamlit web interface

---

## ⚙️ Setup Instructions

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Setup Environment Variables
Create a `.env` file:
```env
OPENAI_API_KEY=your_api_key_here
```

### 3️⃣ Run the Application
```bash
streamlit run main.py
```

---

## 📂 Project Structure

```
ai-chatbot-teacher/
├── src/
│   ├── chatbot.py              # Main chatbot logic
│   ├── language_detector.py    # Language detection
│   └── response_generator.py   # OpenAI response generation
├── main.py                     # Streamlit app
├── requirements.txt
└── README.md
```

---

## 🔍 Example Questions

**English:**
- "What is photosynthesis?"
- "Explain Einstein's theory of relativity"

**Hindi:**
- "डीएनए क्या होता है?"
- "प्रकाश संश्लेषण की व्याख्या करें"

**Telugu:**
- "కృత్రిమ మేధస్సు అంటే ఏమిటి?"
- "కిరణజన్య సంయోగక్రియ అంటే ఏమిటి?"

---

## 🛠 Tech Stack

- **Python 3.8+**
- **OpenAI API** - Response generation
- **langdetect** - Language detection
- **Streamlit** - Web interface

