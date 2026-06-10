import streamlit as st


def init_session_state() -> None:
    defaults = {
        "approved_alerts": [],
        "last_decision": "Nenhuma decisão registrada ainda.",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def register_decision(action: str, approved: bool) -> None:
    decision = "APROVADO" if approved else "REJEITADO"
    text = f"{decision}: {action}"
    st.session_state.last_decision = text
    st.session_state.approved_alerts.append(text)
