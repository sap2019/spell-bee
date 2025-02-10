import streamlit as st
import random

def check_answer(user_answer, correct_answer):
    return user_answer.lower().strip() == correct_answer.lower().strip()

def calculate_section_score(section_answers, correct_answers):
    score = 0
    for user_ans, correct_ans in zip(section_answers, correct_answers):
        if check_answer(user_ans, correct_ans):
            score += 1
    return score

def initialize_session_state():
    if 'current_section' not in st.session_state:
        st.session_state.current_section = 0
    if 'scores' not in st.session_state:
        st.session_state.scores = {
            'dictation': 0,
            'scrambled': 0,
            'missing_letters': 0,
            'word_identification': 0,
            'picture_words': 0
        }
    if 'answers' not in st.session_state:
        st.session_state.answers = {
            'dictation': [''] * 5,
            'scrambled': [''] * 5,
            'missing_letters': [''] * 5,
            'word_identification': [''] * 5,
            'picture_words': [''] * 5
        }
    if 'show_hint' not in st.session_state:
        st.session_state.show_hint = {}

def get_section_name(index):
    sections = ['Dictation', 'Scrambled Words', 'Missing Letters', 
                'Word Identification', 'Picture Words']
    return sections[index]

def display_progress():
    total_sections = 5
    current = st.session_state.current_section
    st.progress(current / total_sections)
    st.write(f"Section {current + 1} of {total_sections}: {get_section_name(current)}")

def display_final_results():
    st.title("Spell Bee Examination Results")
    total_score = sum(st.session_state.scores.values())
    
    st.markdown(f"### Total Score: {total_score}/25")
    
    for section, score in st.session_state.scores.items():
        st.write(f"{section.replace('_', ' ').title()}: {score}/5")
    
    percentage = (total_score / 25) * 100
    if percentage >= 90:
        message = "Outstanding performance! 🌟"
    elif percentage >= 75:
        message = "Great job! 👏"
    elif percentage >= 60:
        message = "Good effort! 👍"
    else:
        message = "Keep practicing! 💪"
    
    st.markdown(f"### {message}")
