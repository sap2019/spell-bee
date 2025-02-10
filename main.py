import streamlit as st
import pandas as pd
import os
from question_handler import generate_test_questions, play_audio
from utils import (initialize_session_state, display_progress, 
                      check_answer, calculate_section_score, display_final_results)
from styles import apply_custom_styles

def reset_session_state():
        st.session_state.submitted = False
        st.session_state.scores = {
            'dictation': 0,
            'scrambled': 0,
            'missing_letters': 0,
            'word_identification': 0,
            'picture_words': 0
        }
        st.session_state.answers = {
            'dictation': [''] * 5,
            'scrambled': [''] * 5,
            'missing_letters': [''] * 5,
            'word_identification': [''] * 5,
            'picture_words': [''] * 5
        }
        st.session_state.show_hint = {}
        # Generate new questions
        st.session_state.questions = generate_test_questions()

def main():
        st.set_page_config(page_title="Interactive Spell Bee Examination", 
                           layout="wide")
        apply_custom_styles()

        initialize_session_state()

        if 'questions' not in st.session_state:
            st.session_state.questions = generate_test_questions()

        if 'submitted' not in st.session_state:
            st.session_state.submitted = False

        st.title("Interactive Spell Bee Examination")

        # Add Load New Questions button when test is completed
        if st.session_state.submitted:
            display_final_results()
            if st.button("Load New Questions", key="load_new"):
                reset_session_state()
                st.rerun()
        else:
            display_all_sections()
            if st.button("Submit All Answers", key="final_submit"):
                calculate_all_scores()
                st.session_state.submitted = True
                st.rerun()

def display_all_sections():
        # Dictation Section
        st.markdown("### 1. Dictation Section")
        st.write("Listen to the word and type it correctly.")

        for i, question in enumerate(st.session_state.questions['dictation']):
            st.markdown(f"#### Question {i + 1}")

            # Audio playback button
            if st.button(f"🔊 Play Word", key=f"play_{i}"):
                audio_path = play_audio(question['audio'])
                if audio_path:
                    st.audio(audio_path)
                else:
                    st.warning("Audio file not found")

            key = f"dictation_{i}"
            user_answer = st.text_input("Your answer:", key=key)
            st.session_state.answers['dictation'][i] = user_answer

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"Show hint {i + 1}", key=f"hint_dict_{i}"):
                    st.info(question['hint'])

        st.markdown("---")

        # Scrambled Section
        st.markdown("### 2. Scrambled Words Section")
        st.write("Unscramble the letters to form the correct word.")

        for i, question in enumerate(st.session_state.questions['scrambled']):
            st.markdown(f"#### Question {i + 1}")
            st.write(f"Scrambled word: {question['scrambled']}")

            key = f"scrambled_{i}"
            user_answer = st.text_input("Your answer:", key=key)
            st.session_state.answers['scrambled'][i] = user_answer

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"Show hint {i + 1}", key=f"hint_scr_{i}"):
                    st.info(question['hint'])

        st.markdown("---")

        # Missing Letters Section
        st.markdown("### 3. Missing Letters Section")
        st.write("Fill in the missing letters to complete the word.")

        for i, question in enumerate(st.session_state.questions['missing_letters']):
            st.markdown(f"#### Question {i + 1}")
            st.write(f"Word with missing letters: {question['display']}")

            key = f"missing_{i}"
            user_answer = st.text_input("Your answer:", key=key)
            st.session_state.answers['missing_letters'][i] = user_answer

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"Show hint {i + 1}", key=f"hint_miss_{i}"):
                    st.info(question['hint'])

        st.markdown("---")

        # Word Identification Section
        st.markdown("### 4. Word Identification Section")
        st.write("Type the correct spelling from the given options.")

        for i, question in enumerate(st.session_state.questions['word_identification']):
            st.markdown(f"#### Question {i + 1}")
            # Display options in the requested format
            options_str = '/'.join(question['options'])
            st.write(f"Options: {options_str}")

            key = f"identification_{i}"
            user_answer = st.text_input("Your answer:", key=key)
            st.session_state.answers['word_identification'][i] = user_answer

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"Show hint {i + 1}", key=f"hint_id_{i}"):
                    st.info(question['hint'])

        st.markdown("---")

        # Picture Words Section
        st.markdown("### 5. Picture Words Section")
        st.write("Write the word that corresponds to each picture.")

        for i, question in enumerate(st.session_state.questions['picture_words']):
            st.markdown(f"#### Question {i + 1}")
            picture_path = os.path.join('pictures', question['image'])
            if os.path.exists(picture_path):
                # Set max width to 400 pixels while maintaining aspect ratio
                st.image(picture_path, caption='', width=400)
            else:
                st.error(f"Image not found: {question['image']}")

            key = f"picture_{i}"
            user_answer = st.text_input("Your answer:", key=key)
            st.session_state.answers['picture_words'][i] = user_answer

            col1, col2 = st.columns([3, 1])
            with col2:
                if st.button(f"Show hint {i + 1}", key=f"hint_pic_{i}"):
                    st.info(question['hint'])

def calculate_all_scores():
        for section in ['dictation', 'scrambled', 'missing_letters', 'word_identification', 'picture_words']:
            score = calculate_section_score(
                st.session_state.answers[section],
                [q['word'] if section != 'word_identification' else q['correct'] 
                 for q in st.session_state.questions[section]]
            )
            st.session_state.scores[section] = score

if __name__ == "__main__":
        main()