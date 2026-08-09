"""
Question Engine page for the Context Assembly Framework.
This page demonstrates the dynamic question rendering capability.
"""

from typing import Any

import streamlit as st

from caf.services import question_service


def render_question(question: dict) -> Any:
    """Render a single question based on its type and return the answer.

    Args:
        question: Dictionary containing question configuration

    Returns:
        User's answer to the question
    """
    q_id = question["id"]
    q_text = question["text"]
    q_type = question["type"]
    required = question.get("required", False)
    placeholder = question.get("placeholder", "")

    # Add required indicator if needed
    if required:
        q_text = f"**{q_text}*"

    if q_type == "text":
        return st.text_input(label=q_text, key=q_id, placeholder=placeholder)

    elif q_type == "select":
        options = question.get("options", [])
        return st.selectbox(
            label=q_text,
            options=options,
            key=q_id,
            placeholder="Select an option" if not required else None,
        )

    elif q_type == "multiselect":
        options = question.get("options", [])
        return st.multiselect(label=q_text, options=options, key=q_id)

    else:
        # Default to text input for unknown types
        return st.text_input(label=q_text, key=q_id, placeholder=placeholder)


def main():
    """Main function for the Question Engine page."""
    st.set_page_config(
        page_title="Question Engine - CAF", page_icon="❓", layout="wide"
    )

    st.title("❓ Question Engine Demo")
    st.markdown("---")

    # Introduction
    st.markdown("""
    This page demonstrates the dynamic question rendering capability of the Context Assembly Framework.
    Questions are loaded from a JSON configuration and rendered based on their type.
    """)

    # Load questions
    questions = question_service.get_all_questions()

    if not questions:
        st.error("No questions found. Please check the question configuration.")
        return

    # Form for submitting answers
    with st.form("questionnaire_form"):
        st.subheader("Please answer the following questions:")

        answers = {}

        # Render each question
        for question in questions:
            answer = render_question(question)
            answers[question["id"]] = answer

        # Submit button
        submitted = st.form_submit_button("Submit Answers")

        if submitted:
            # Validate answers
            validation_errors = []
            for question in questions:
                q_id = question["id"]
                answer = answers.get(q_id)
                if not question_service.validate_answer(question, answer):
                    validation_errors.append(
                        f"Please answer '{question['text']}' correctly."
                    )

            if validation_errors:
                for error in validation_errors:
                    st.error(error)
            else:
                # Store answers in session state
                st.session_state.answers = answers
                st.success("Thank you for your responses!")

                # Display submitted answers
                st.subheader("Your Responses:")
                for question in questions:
                    q_id = question["id"]
                    answer = answers.get(q_id)
                    st.write(f"**{question['text']}**")
                    if isinstance(answer, list):
                        if answer:
                            st.write(", ".join(map(str, answer)))
                        else:
                            st.write("*No selection*")
                    else:
                        st.write(answer if answer else "*No response*")
                    st.write("")  # Add spacing


if __name__ == "__main__":
    main()
