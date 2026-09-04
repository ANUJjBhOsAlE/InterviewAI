# 🤖 InterviewAI

InterviewAI is an AI-powered interview preparation application built with
Python and Streamlit. It helps users practice technical interviews,
evaluate their answers, and receive AI-generated feedback.

The application can also analyze a user's resume and generate
resume-based interview questions.

---

## 🚀 Features

### 🎯 Interview Practice
- Select your target job role
- Choose difficulty level
- Choose interview level
- Get dynamically generated interview questions
- Navigate between questions
- Submit answers for AI evaluation

### 🧠 AI Answer Evaluation
Each answer is evaluated using multiple parameters:

- Accuracy
- Relevance
- Completeness
- Clarity
- Overall Score
- Personalized Feedback

### 📄 Resume Analysis
- Upload a PDF resume
- Extract resume content
- Analyze skills and technologies
- Identify programming languages
- Identify projects and experience
- Generate resume-based interview questions

### 📊 Interview Report
After completing the interview, users receive:

- Average scores
- Question-wise evaluation
- Individual feedback
- Overall interview summary
- Interview details

---

## 👨‍💻 Supported Roles

InterviewAI currently supports interview preparation for roles such as:

- Python Developer
- Data Analyst
- Software Engineer
- Machine Learning Engineer

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit**
- **Google Gemini AI**
- **PDF Text Extraction**
- **Python Libraries & APIs**

---

## 📁 Project Structure

```text
InterviewAI/
│
├── data/
│   └── Application data/resources
│
├── services/
│   └── AI and application services
│
├── utils/
│   └── Helper and utility functions
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md