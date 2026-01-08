import streamlit as st
from components.sidebar import sidebar_ui
from components.chat_ui import chat_ui
from components.pdf_handler import handle_pdf_upload

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="StudyBuddy AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Global UI Theme (Dark SaaS Style)
# -------------------------------------------------
st.markdown("""
<style>
/* App background */
.stApp {
    background: radial-gradient(circle at top left, #0f172a, #020617);
    color: #e5e7eb;
}

/* Main Title */
.main-title {
    font-size: 44px;
    font-weight: 800;
    margin-bottom: 6px;
}
.subtitle {
    font-size: 18px;
    color: #9ca3af;
    margin-bottom: 28px;
}

/* Cards */
.card {
    background: rgba(255,255,255,0.06);
    border-radius: 18px;
    padding: 22px;
    margin-bottom: 22px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Divider spacing */
hr {
    margin: 30px 0;
}

/* Buttons */
.stButton button {
    border-radius: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# Session State Initialization
# -------------------------------------------------
if "pdf_content" not in st.session_state:
    st.session_state.pdf_content = None
if "user_focus" not in st.session_state:
    st.session_state.user_focus = ""

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
selected_mode, selected_sub_mode = sidebar_ui()

# -------------------------------------------------
# Header Section
# -------------------------------------------------
st.markdown("""
<div class="main-title">🧠 StudyBuddy AI</div>
<div class="subtitle">
Your smart AI-powered study assistant for explanations, summaries, and exams
</div>
""", unsafe_allow_html=True)

st.markdown("✅ **Gemini 2.5 Flash** &nbsp;&nbsp; ⚡ **Fast Responses** &nbsp;&nbsp; 🔒 **Secure API**")

# -------------------------------------------------
# PDF Upload Section (Card Layout)
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("### 📚 Upload Study Material (Optional)")
pdf_text, user_focus, summarize_clicked = handle_pdf_upload()
st.markdown('</div>', unsafe_allow_html=True)

if summarize_clicked and pdf_text:
    st.session_state.pdf_content = pdf_text
    st.session_state.user_focus = user_focus
    st.success("✅ PDF loaded successfully! You can now chat for summaries or explanations.")

st.divider()

# -------------------------------------------------
# Chat Section
# -------------------------------------------------
st.markdown('<div class="card">', unsafe_allow_html=True)
chat_ui(selected_mode, selected_sub_mode)
st.markdown('</div>', unsafe_allow_html=True)

# -------------------------------------------------
# Footer
# -------------------------------------------------
st.markdown("""
<hr>
<center style="color:#9ca3af; font-size:14px;">
Made with ❤️ by <b>Alok Kumar</b> · StudyBuddy AI
</center>
""", unsafe_allow_html=True)
