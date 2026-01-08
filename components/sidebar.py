import streamlit as st
import time

def sidebar_ui():
    """Premium sidebar with mode selection and controls."""

    # -------------------------------------------------
    # Sidebar Header
    # -------------------------------------------------
    st.sidebar.markdown("## 🧠 StudyBuddy AI")
    st.sidebar.caption("Your smart AI study assistant")

    st.sidebar.markdown("---")

    # -------------------------------------------------
    # Model Info Card
    # -------------------------------------------------
    st.sidebar.markdown("### ⚡ AI Model")
    st.sidebar.info("🚀 **Gemini 2.5 Flash**")

    st.sidebar.markdown("---")

    # -------------------------------------------------
    # Mode Selection
    # -------------------------------------------------
    st.sidebar.markdown("### 🧩 Learning Mode")

    mode = st.sidebar.radio(
    "Select Mode",
    ["💡 Explainer", "📰 Summarizer", "🧩 Quizzer"],
    label_visibility="collapsed"
)

    # -------------------------------------------------
    # Quizzer Sub-modes
    # -------------------------------------------------
    sub_mode = st.sidebar.radio(
    "Quizzer Options",
    [
        "📝 Generate Questions",
        "📖 Solve Questions",
        "✅ Evaluate Answers"
    ],
    label_visibility="collapsed"
)


    st.sidebar.markdown("---")

    # -------------------------------------------------
    # New Chat Button
    # -------------------------------------------------
    if st.sidebar.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        success_placeholder = st.sidebar.empty()
        with success_placeholder:
            st.success("New chat started!")
        time.sleep(1.5)
        success_placeholder.empty()

    

    st.sidebar.caption("✨ Built with Streamlit & Gemini")

    return mode, sub_mode
