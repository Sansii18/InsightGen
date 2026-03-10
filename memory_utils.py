import streamlit as st


def init_memory():
    """Ensure session state keys exist for conversational memory."""
    if "previous_sql" not in st.session_state:
        st.session_state.previous_sql = None
    if "previous_df" not in st.session_state:
        st.session_state.previous_df = None
    if "chat_history" not in st.session_state:
        # store tuples of (question, sql) so we can feed context back to LLM
        st.session_state.chat_history = []


def update_memory(question: str, sql: str, df):
    """Record the latest interaction."""
    st.session_state.previous_sql = sql
    st.session_state.previous_df = df
    st.session_state.chat_history.append((question, sql))


def get_context_prompt():
    """Return a formatted string representing the conversation so far."""
    parts = []
    for q, s in st.session_state.chat_history:
        parts.append(f"User question: {q}\nSQL: {s}")
    return "\n\n".join(parts)
