import streamlit as st
import re
from collections import Counter

st.set_page_config(
    page_title="AI Resume & Job Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume & Job Description Analyzer")
st.write(
    "Analyze how well your resume matches a job description "
    "and identify important skills and keywords."
)

# Common technical and professional skills
SKILLS = {
    "python", "java", "javascript", "sql", "excel", "power bi",
    "tableau", "machine learning", "deep learning", "data analysis",
    "data visualization", "statistics", "pandas", "numpy", "tensorflow",
    "pytorch", "git", "github", "html", "css", "react", "aws",
    "azure", "communication", "leadership", "teamwork", "problem solving",
    "project management", "research", "marketing", "sales", "finance",
    "accounting", "management", "analytics", "artificial intelligence",
    "natural language processing", "data annotation"
}

def clean_text(text):
    return re.findall(r"\b[a-zA-Z][a-zA-Z+#.-]{2,}\b", text.lower())

def find_skills(text):
    text_lower = text.lower()
    return {skill for skill in SKILLS if skill in text_lower}

def get_keywords(text):
    words = clean_text(text)
    stop_words = {
        "the", "and", "for", "with", "that", "this", "from",
        "are", "you", "your", "will", "have", "has", "our",
        "their", "about", "into", "using", "years", "work",
        "job", "role", "required", "preferred"
    }

    return Counter(
        word for word in words
        if word not in stop_words and len(word) > 3
    )

resume = st.text_area(
    "📄 Paste your Resume",
    height=300,
    placeholder="Paste your resume text here..."
)

job_description = st.text_area(
    "💼 Paste the Job Description",
    height=300,
    placeholder="Paste the job description here..."
)

if st.button("🔍 Analyze Resume", use_container_width=True):

    if not resume.strip() or not job_description.strip():
        st.warning("Please enter both your resume and the job description.")

    else:
        resume_words = set(clean_text(resume))
        job_words = set(clean_text(job_description))

        matching_words = resume_words.intersection(job_words)
        missing_words = job_words - resume_words

        if job_words:
            keyword_score = round(
                len(matching_words) / len(job_words) * 100, 1
            )
        else:
            keyword_score = 0

        resume_skills = find_skills(resume)
        job_skills = find_skills(job_description)

        matching_skills = resume_skills.intersection(job_skills)
        missing_skills = job_skills - resume_skills

        if job_skills:
            skill_score = round(
                len(matching_skills) / len(job_skills) * 100, 1
            )
        else:
            skill_score = 0

        overall_score = round(
            (keyword_score * 0.5) + (skill_score * 0.5), 1
        )

        st.divider()
        st.subheader("📊 Resume Match Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Overall Match", f"{overall_score}%")

        with col2:
            st.metric("Keyword Match", f"{keyword_score}%")

        with col3:
            st.metric("Skill Match", f"{skill_score}%")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("✅ Matching Skills")

            if matching_skills:
                for skill in sorted(matching_skills):
                    st.write(f"• {skill}")
            else:
                st.write("No matching skills detected.")

        with col2:
            st.subheader("⚠️ Potentially Missing Skills")

            if missing_skills:
                for skill in sorted(missing_skills):
                    st.write(f"• {skill}")
            else:
                st.write("No major missing skills detected.")

        st.divider()

        st.subheader("🔑 Important Job Keywords")

        job_keywords = get_keywords(job_description)

        if job_keywords:
            important = [
                word for word, count in job_keywords.most_common(20)
            ]
            st.write(", ".join(important))

        st.subheader("💡 Resume Improvement Suggestions")

        if overall_score < 50:
            st.write(
                "• Your resume has a relatively low match with this job. "
                "Consider tailoring your skills and experience to the role."
            )
            st.write(
                "• Review the missing skills above and add relevant "
                "experience only if you genuinely have it."
            )

        elif overall_score < 75:
            st.write(
                "• Your resume has a moderate match. Consider improving "
                "the wording of relevant experience and skills."
            )
            st.write(
                "• Make sure important qualifications from the job "
                "description are clearly represented where truthful."
            )

        else:
            st.write(
                "• Your resume has a strong match with this job description."
            )
            st.write(
                "• Keep the resume concise and make your strongest "
                "relevant achievements easy to find."
            )

        st.caption(
            "Note: This is a keyword-based analysis tool and does not "
            "guarantee an employer's actual ATS score."
        )
