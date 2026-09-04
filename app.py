from services.question_engine import get_questions
from services.evaluator import evaluate_answer
from services.resume_parser import extract_resume_text
from services.resume_analyzer import analyze_resume

import streamlit as st


# -------------------------------
# PAGE CONFIG
# -------------------------------

st.set_page_config(
    page_title="InterviewAI",
    page_icon="🤖",
    layout="centered"
)


# -------------------------------
# HEADER
# -------------------------------

st.title("🤖 InterviewAI")
st.subheader("AI-Powered Mock Interview Platform")

st.write(
    "Practice technical interviews and get personalized "
    "feedback on your answers."
)

st.divider()


# -------------------------------
# RESUME UPLOAD
# -------------------------------

st.subheader("📄 Resume")

resume_file = st.file_uploader(
    "Upload your resume (PDF)",
    type=["pdf"]
)


if resume_file:

    resume_text = extract_resume_text(resume_file)

    if resume_text:

        st.success("✅ Resume uploaded successfully!")

        st.session_state["resume_text"] = resume_text

        with st.expander("📋 Preview Resume Text"):
            st.write(resume_text)


        # -------------------------------
        # ANALYZE RESUME
        # -------------------------------

        if st.button(
            "🧠 Analyze Resume",
            use_container_width=True
        ):

            with st.spinner("Analyzing resume with AI..."):

                analysis = analyze_resume(resume_text)

                st.session_state["resume_analysis"] = analysis

            st.success("Resume analyzed successfully!")


# -------------------------------
# RESUME ANALYSIS
# -------------------------------

if st.session_state.get("resume_analysis"):

    analysis = st.session_state["resume_analysis"]

    st.divider()

    st.subheader("🧠 Resume Analysis")


    st.write("### 💻 Technical Skills")

    st.write(
        ", ".join(analysis["skills"])
    )


    st.write("### 🐍 Programming Languages")

    st.write(
        ", ".join(analysis["languages"])
    )


    st.write("### 🛠️ Technologies")

    st.write(
        ", ".join(analysis["technologies"])
    )


    st.write("### 📂 Projects")

    for project in analysis["projects"]:

        st.write(
            f"• {project}"
        )


    st.write("### 💼 Experience")

    for experience in analysis["experience"]:

        st.write(
            f"• {experience}"
        )


    st.divider()

    st.subheader("🎯 Personalized Interview Questions")


    for i, question in enumerate(
        analysis["questions"]
    ):

        st.write(
            f"**{i + 1}. {question}**"
        )


    # -------------------------------
    # START RESUME INTERVIEW
    # -------------------------------

    if st.button(
        "🎯 Start Resume-Based Interview",
        use_container_width=True
    ):

        resume_questions = analysis["questions"]

        st.session_state["questions"] = resume_questions
        st.session_state["current_question"] = 0
        st.session_state["answers"] = []
        st.session_state["current_evaluation"] = None

        st.session_state["started"] = True
        st.session_state["interview_completed"] = False

        st.session_state["resume_based"] = True

        st.rerun()


# -------------------------------
# INTERVIEW SETUP
# -------------------------------

st.divider()

st.subheader("⚙️ Interview Setup")


role = st.selectbox(
    "Select Job Role",
    [
        "Python Developer",
        "Data Analyst",
        "Software Engineer",
        "Machine Learning Engineer"
    ]
)


experience = st.selectbox(
    "Experience Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


difficulty = st.select_slider(
    "Interview Difficulty",
    options=[
        "Easy",
        "Medium",
        "Hard"
    ],
    value="Medium"
)


# -------------------------------
# START NORMAL INTERVIEW
# -------------------------------

if st.button(
    "🚀 Start Interview",
    use_container_width=True
):

    questions = get_questions(
        role,
        experience,
        difficulty,
        count=5
    )


    st.session_state["role"] = role
    st.session_state["experience"] = experience
    st.session_state["difficulty"] = difficulty

    st.session_state["questions"] = questions

    st.session_state["current_question"] = 0

    st.session_state["answers"] = []

    st.session_state["current_evaluation"] = None

    st.session_state["started"] = True

    st.session_state["interview_completed"] = False

    st.session_state["resume_based"] = False

    st.rerun()


# -------------------------------
# INTERVIEW
# -------------------------------

if st.session_state.get("started"):

    questions = st.session_state["questions"]

    current = st.session_state["current_question"]


    st.divider()


    # -------------------------------
    # QUESTION HEADER
    # -------------------------------

    if st.session_state.get("resume_based"):

        st.subheader(
            f"📄 Resume Question "
            f"{current + 1} of {len(questions)}"
        )

    else:

        st.subheader(
            f"Question "
            f"{current + 1} of {len(questions)}"
        )


    # -------------------------------
    # QUESTION
    # -------------------------------

    st.write(
        questions[current]
    )


    # -------------------------------
    # ANSWER BOX
    # -------------------------------

    answer = st.text_area(
        "Your Answer",
        key=f"answer_{current}",
        placeholder="Type your answer here..."
    )


    # -------------------------------
    # SUBMIT ANSWER
    # -------------------------------

    if st.button(
        "Submit Answer",
        use_container_width=True
    ):

        if answer.strip():

            result = evaluate_answer(
                questions[current],
                answer
            )


            st.session_state["answers"].append({

                "question": questions[current],

                "answer": answer,

                "evaluation": result

            })


            st.session_state["current_evaluation"] = result

            st.rerun()


        else:

            st.warning(
                "Please enter your answer."
            )


    # -------------------------------
    # SHOW EVALUATION
    # -------------------------------

    if st.session_state.get(
        "current_evaluation"
    ):

        result = st.session_state[
            "current_evaluation"
        ]


        st.divider()

        st.subheader(
            "📊 Answer Evaluation"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Accuracy",
                f"{result['accuracy']}/10"
            )

            st.metric(
                "Relevance",
                f"{result['relevance']}/10"
            )


        with col2:

            st.metric(
                "Completeness",
                f"{result['completeness']}/10"
            )

            st.metric(
                "Clarity",
                f"{result['clarity']}/10"
            )


        st.metric(
            "Overall Score",
            f"{result['overall']}/10"
        )


        st.info(
            f"💡 Feedback: "
            f"{result['feedback']}"
        )


        st.divider()


        # -------------------------------
        # NEXT QUESTION
        # -------------------------------

        if current + 1 < len(questions):

            if st.button(
                "➡️ Next Question",
                use_container_width=True
            ):

                st.session_state[
                    "current_question"
                ] += 1


                st.session_state[
                    "current_evaluation"
                ] = None


                st.rerun()


        # -------------------------------
        # FINISH INTERVIEW
        # -------------------------------

        else:

            if st.button(
                "🏁 Finish Interview",
                use_container_width=True
            ):

                st.session_state[
                    "interview_completed"
                ] = True

                st.session_state[
                    "started"
                ] = False

                st.rerun()


# -------------------------------
# FINAL INTERVIEW REPORT
# -------------------------------

if st.session_state.get(
    "interview_completed"
):

    st.divider()

    st.title(
        "📊 Final Interview Report"
    )


    answers = st.session_state.get(
        "answers",
        []
    )


    if answers:

        # -------------------------------
        # CALCULATE SCORES
        # -------------------------------

        total_accuracy = 0

        total_relevance = 0

        total_completeness = 0

        total_clarity = 0

        total_overall = 0


        for item in answers:

            evaluation = item[
                "evaluation"
            ]


            total_accuracy += evaluation[
                "accuracy"
            ]

            total_relevance += evaluation[
                "relevance"
            ]

            total_completeness += evaluation[
                "completeness"
            ]

            total_clarity += evaluation[
                "clarity"
            ]

            total_overall += evaluation[
                "overall"
            ]


        total_questions = len(answers)


        avg_accuracy = (
            total_accuracy /
            total_questions
        )


        avg_relevance = (
            total_relevance /
            total_questions
        )


        avg_completeness = (
            total_completeness /
            total_questions
        )


        avg_clarity = (
            total_clarity /
            total_questions
        )


        avg_overall = (
            total_overall /
            total_questions
        )


        # -------------------------------
        # OVERALL SCORE
        # -------------------------------

        st.subheader(
            "🏆 Overall Performance"
        )


        st.metric(
            "Overall Score",
            f"{avg_overall:.1f}/10"
        )


        # -------------------------------
        # SCORE BREAKDOWN
        # -------------------------------

        st.subheader(
            "📈 Score Breakdown"
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Accuracy",
                f"{avg_accuracy:.1f}/10"
            )

            st.metric(
                "Completeness",
                f"{avg_completeness:.1f}/10"
            )


        with col2:

            st.metric(
                "Relevance",
                f"{avg_relevance:.1f}/10"
            )

            st.metric(
                "Clarity",
                f"{avg_clarity:.1f}/10"
            )


        # -------------------------------
        # QUESTION PERFORMANCE
        # -------------------------------

        st.divider()

        st.subheader(
            "📝 Question-wise Performance"
        )


        for index, item in enumerate(
            answers
        ):

            evaluation = item[
                "evaluation"
            ]


            st.write(
                f"### Question {index + 1}"
            )


            st.write(
                item["question"]
            )


            st.write(
                f"**Overall Score:** "
                f"{evaluation['overall']}/10"
            )


            st.progress(
                evaluation["overall"] / 10
            )


            with st.expander(
                "View Answer & Feedback"
            ):

                st.write(
                    "**Your Answer:**"
                )

                st.write(
                    item["answer"]
                )


                st.write(
                    "**AI Feedback:**"
                )

                st.info(
                    evaluation["feedback"]
                )


        # -------------------------------
        # PERFORMANCE SUMMARY
        # -------------------------------

        st.divider()

        st.subheader(
            "💡 Performance Summary"
        )


        if avg_overall >= 8:

            st.success(
                "Excellent performance! "
                "You demonstrated strong "
                "understanding of the "
                "interview topics."
            )


        elif avg_overall >= 6:

            st.warning(
                "Good performance! "
                "You have a decent "
                "understanding, but there "
                "is room for improvement."
            )


        else:

            st.error(
                "More practice is recommended. "
                "Focus on strengthening your "
                "fundamentals."
            )


        # -------------------------------
        # INTERVIEW DETAILS
        # -------------------------------

        st.divider()

        st.subheader(
            "📋 Interview Details"
        )


        st.write(
            f"**Job Role:** "
            f"{st.session_state.get('role', 'Resume-Based')}"
        )


        st.write(
            f"**Experience Level:** "
            f"{st.session_state.get('experience', 'N/A')}"
        )


        st.write(
            f"**Difficulty:** "
            f"{st.session_state.get('difficulty', 'N/A')}"
        )


        st.write(
            f"**Questions Attempted:** "
            f"{total_questions}"
        )