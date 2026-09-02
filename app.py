import streamlit as st
import re

st.set_page_config(
    page_title="AI Resume & Job Analyzer",
    page_icon="📄"
)

st.title("📄 AI Resume & Job Description Analyzer")
st.write(
    "Compare your resume with a job description and identify important keywords."
)

resume = st.text_area("Paste your Resume", height=250)
job_description = st.text_area("Paste the Job Description", height=250)

if st.button("Analyze"):
    if not resume or not job_description:
        st.warning("Please enter both your resume and the job description.")
    else:
        resume_words = set(
            re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", resume.lower())
        )
        job_words = set(
            re.findall(
                r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b",
                job_description.lower()
            )
        )

        matching = resume_words.intersection(job_words)
        missing = job_words - resume_words

        score = round((len(matching) / len(job_words)) * 100, 1)

        st.subheader(f"ATS Keyword Match: {score}%")

        st.write("### ✅ Matching Keywords")
        st.write(
            ", ".join(sorted(matching))
            if matching
            else "None found."
        )

        st.write("### ⚠️ Potentially Missing Keywords")
        st.write(
            ", ".join(sorted(list(missing)[:30]))
            if missing
            else "None."
        )

        st.write("### 💡 Suggestions")

        if score < 50:
            st.write(
                "Consider adding relevant skills and terminology "
                "from the job description."
            )
        elif score < 75:
            st.write(
                "Your resume has a reasonable keyword match. "
                "Review the potentially missing keywords."
            )
        else:
            st.write(
                "Your resume has a strong keyword match. "
                "Continue tailoring it to the role."
            )
