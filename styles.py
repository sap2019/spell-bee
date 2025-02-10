import streamlit as st

def apply_custom_styles():
    st.markdown("""
        <style>
        .main {
            padding: 2rem;
        }
        .stButton>button {
            width: 100%;
            margin: 1rem 0;
        }
        .question-box {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
        }
        .hint-text {
            color: #666;
            font-style: italic;
        }
        .score-display {
            font-size: 1.5rem;
            font-weight: bold;
            color: #1f77b4;
        }
        </style>
    """, unsafe_allow_html=True)
