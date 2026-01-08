"""
StudyBuddy AI
Author: Alok Kumar
Description: AI-powered study assistant built with Streamlit & Gemini
"""


import streamlit as st
from PyPDF2 import PdfReader

def handle_pdf_upload():
    """
    Handles PDF upload with editable extraction.
    Returns tuple: (pdf_text, user_extra_prompt, summarize_clicked)
    """

    # ---------------------------------------------
    # Upload Section
    # ---------------------------------------------
    st.markdown("### 📚 Upload Study Material (PDF)")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=["pdf"],
        label_visibility="collapsed"
    )

    pdf_text = ""
    user_extra = ""

    if not uploaded_file:
        st.caption("Upload lecture notes, textbooks, or hand-written PDFs (text-based).")
        return None, None, False

    # ---------------------------------------------
    # PDF Extraction
    # ---------------------------------------------
    with st.spinner("📖 Extracting text from PDF..."):
        try:
            reader = PdfReader(uploaded_file)
            for page in reader.pages:
                pdf_text += page.extract_text() or ""
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")
            return None, None, False

    st.success("✅ PDF processed successfully!")

    # ---------------------------------------------
    # Session State Handling
    # ---------------------------------------------
    preview = pdf_text[:3000] if pdf_text else ""
    file_name = uploaded_file.name

    if (
        "pdf_raw" not in st.session_state
        or st.session_state.get("last_upload_name") != file_name
    ):
        st.session_state["pdf_raw"] = pdf_text
        st.session_state["pdf_edited"] = preview
        st.session_state["last_upload_name"] = file_name

    # ---------------------------------------------
    # Editable Text Preview
    # ---------------------------------------------
    st.markdown("### ✍️ Review & Edit Extracted Text")

    st.text_area(
        "You can trim, edit, or add notes below:",
        value=st.session_state.get("pdf_edited", preview),
        height=280,
        key="pdf_edited",
        help="Editing helps improve summarization quality"
    )

    raw_len = len(st.session_state.get("pdf_raw", "").strip())
    edited_len = len(st.session_state.get("pdf_edited", "").strip())

    st.caption(
        f"📊 Extracted text: **{raw_len} chars** · "
        f"Current editable text: **{edited_len} chars**"
    )

    if raw_len < 50:
        st.warning(
            "⚠️ Very little text detected. "
            "If this is a scanned PDF, use OCR before uploading."
        )

    # ---------------------------------------------
    # Customization Options
    # ---------------------------------------------
    st.markdown("### 🎯 Summary Preferences")

    user_extra = st.text_input(
        "How should StudyBuddy summarize this?",
        placeholder="Example: exam-oriented, key points only, explain with examples",
        help="This guides the AI while summarizing"
    )

    # ---------------------------------------------
    # Action Buttons
    # ---------------------------------------------
    col1, col2 = st.columns([1, 1])

    with col1:
        summarize_clicked = st.button(
            "🚀 Generate Summary",
            use_container_width=True,
            key="summarize_btn"
        )

    with col2:
        clear_clicked = st.button(
            "🗑️ Clear PDF",
            use_container_width=True,
            key="clear_btn"
        )

    if clear_clicked:
        for k in ("pdf_raw", "pdf_edited", "last_upload_name"):
            if k in st.session_state:
                del st.session_state[k]
        st.rerun()

    # ---------------------------------------------
    # Decide Final Text to Summarize
    # ---------------------------------------------
    if summarize_clicked:
        edited = st.session_state.get("pdf_edited", "").strip()
        raw = st.session_state.get("pdf_raw", "").strip()
        preview_of_raw = raw[:3000]

        if not edited and raw:
            text_to_summarize = raw
        elif edited == preview_of_raw:
            text_to_summarize = raw
        else:
            text_to_summarize = edited

        if text_to_summarize and len(text_to_summarize) >= 50:
            return text_to_summarize, user_extra, True
        else:
            st.error(
                "❌ Not enough valid text to summarize. "
                "Please check the extracted content."
            )
            return None, None, False

    return st.session_state.get("pdf_edited", preview), user_extra, False
