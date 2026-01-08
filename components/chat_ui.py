import streamlit as st
from core.explainer import explain_concept
from core.summarizer import summarize_text
from core.quizzer import (
    generate_questions,
    solve_questions,
    evaluate_answers
)

# -------------------------------------------------
# Helper: context from previous messages
# -------------------------------------------------
def get_previous_messages_summary(messages, limit=3):
    context_messages = messages[-2 * limit:]
    return "\n".join(
        f"{m['role'].capitalize()}: {m['content']}" for m in context_messages
    )

# -------------------------------------------------
# Main Chat UI
# -------------------------------------------------
def chat_ui(selected_mode, selected_sub_mode=None):

    # Header
    if selected_sub_mode:
        st.markdown(
            f"### 💬 StudyBuddy Chat — {selected_mode} · {selected_sub_mode}"
        )
    else:
        st.markdown(
            f"### 💬 StudyBuddy Chat — {selected_mode}"
        )

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # -------------------------------------------------
    # Display chat history (Custom Bubbles)
    # -------------------------------------------------
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"""
                <div class="chat-user">
                    🧑 {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"""
                <div class="chat-ai">
                    🤖 {msg["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

    # -------------------------------------------------
    # User Input
    # -------------------------------------------------
    prompt = st.chat_input("Type your message…")

    if not prompt:
        return

    # Save user message
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    st.markdown(
        f"""
        <div class="chat-user">
            🧑 {prompt}
        </div>
        """,
        unsafe_allow_html=True
    )

    previous_context = get_previous_messages_summary(
        st.session_state.messages[:-1],
        limit=3
    )

    assistant_response = ""

    # -------------------------------------------------
    # AI Processing
    # -------------------------------------------------
    with st.spinner("💡 StudyBuddy is thinking…"):
        try:
            if selected_mode == "💡 Explainer":
                assistant_response = explain_concept(
                    prompt, previous_context
                )

            elif selected_mode == "📰 Summarizer":
                pdf = st.session_state.get("pdf_content")
                user_focus = st.session_state.get("user_focus", "")

                p = prompt.strip()
                first_word = p.split()[0].lower() if p else ""
                is_short = len(p.split()) <= 12
                is_question = (
                    p.endswith("?")
                    or first_word in (
                        "what", "why", "how", "when",
                        "which", "who", "where",
                        "explain", "describe"
                    )
                )
                is_followup = bool(p) and (is_short or is_question)

                if pdf:
                    if is_followup:
                        extra = (
                            f"Follow-up question: {p}. "
                            "Use previous response and PDF content."
                        )
                    else:
                        extra = p or user_focus

                    assistant_response = summarize_text(
                        text=pdf,
                        previous_context=previous_context,
                        user_focus=user_focus,
                        extra_instruction=extra
                    )
                else:
                    assistant_response = summarize_text(
                        p, previous_context
                    )

            elif selected_mode == "🧩 Quizzer":
                if selected_sub_mode == "📝 Generate Questions":
                    st.info(
                        "📘 Enter a topic or passage. "
                        "Questions come first, answers at the end."
                    )
                    assistant_response = generate_questions(
                        prompt, previous_context
                    )

                elif selected_sub_mode == "📖 Solve Questions":
                    st.info(
                        "📝 Paste exam questions. "
                        "Include marks/limits if required."
                    )
                    assistant_response = solve_questions(
                        prompt, previous_context
                    )

                elif selected_sub_mode == "✅ Evaluate Answers":
                    qs_ans = prompt.split("---")
                    if len(qs_ans) != 2:
                        assistant_response = (
                            "⚠️ Please separate questions and answers "
                            "using `---`."
                        )
                    else:
                        assistant_response = evaluate_answers(
                            qs_ans[0].strip(),
                            qs_ans[1].strip(),
                            previous_context
                        )
                else:
                    assistant_response = "⚠️ Unknown Quizzer sub-mode."

            else:
                assistant_response = "⚠️ Unknown mode selected."

        except Exception as e:
            assistant_response = (
                "❌ Something went wrong. Please try again.\n\n"
                f"Error: {str(e)}"
            )

    # -------------------------------------------------
    # Display AI Response
    # -------------------------------------------------
    st.markdown(
        f"""
        <div class="chat-ai">
            🤖 {assistant_response}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Save assistant message
    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_response}
    )

    # -------------------------------------------------
    # Feedback Section
    # -------------------------------------------------
    st.markdown("**Was this response helpful?**")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("👍 Helpful", key=f"fb_yes_{len(st.session_state.messages)}"):
            st.success("Thanks for the feedback!")

    with col2:
        if st.button("👎 Not Helpful", key=f"fb_no_{len(st.session_state.messages)}"):
            st.info("We’ll try to improve the next response.")

            """
StudyBuddy AI
Author: Alok Kumar
"""

