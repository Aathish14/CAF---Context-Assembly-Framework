import streamlit as st
from caf.services.context_builder import ContextBuilder
from caf.services.question_service import question_service
from caf.services.validation_service import validation_service
from caf.core.container import get_container


def main():
    st.set_page_config(
        page_title="Context Assembly Framework (CAF) - Workflow Demo",
        page_icon="🏭",
        layout="wide",
    )

    st.title("Context Assembly Framework (CAF)")
    st.caption("End-to-end demonstration of the CAF workflow.")

    # Initialize session state
    if "context" not in st.session_state:
        st.session_state.context = None
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "selected_template_id" not in st.session_state:
        st.session_state.selected_template_id = None
    if "instruction" not in st.session_state:
        st.session_state.instruction = None
    if "version" not in st.session_state:
        st.session_state.version = None
    if "container" not in st.session_state:
        st.session_state.container = None

    # Get all questions
    questions = question_service.get_all_questions()
    if not questions:
        st.error("No questions configured. Please check the questions.json file.")
        return

    # Sidebar for status
    with st.sidebar:
        st.header("CAF Status")
        if st.session_state.context is None:
            st.info("Session: Awaiting context")
        elif st.session_state.instruction is None:
            st.info("Session: Context created")
        elif st.session_state.version is None:
            st.info("Session: Instruction generated")
        else:
            st.success("Session: Version created")
        if st.button("Reset Session"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    # Step 1: Question Engine
    st.header("Step 1: Define Context")
    with st.form(key="question_form"):
        st.subheader("Answer the following questions")
        answers = {}
        for question in questions:
            q_id = question["id"]
            q_text = question["text"]
            q_type = question["type"]
            required = question.get("required", False)
            display_text = f"{q_text} {'*' if required else ''}"
            if q_type == "text":
                placeholder = question.get("placeholder", "")
                answer = st.text_input(
                    label=display_text, key=q_id, placeholder=placeholder
                )
                answers[q_id] = answer
            elif q_type == "select":
                options = question.get("options", [])
                if required and "" not in options:
                    options = [""] + options
                answer = st.selectbox(
                    label=display_text, options=options, key=q_id
                )
                answers[q_id] = answer
            elif q_type == "multiselect":
                options = question.get("options", [])
                answer = st.multiselect(
                    label=display_text, options=options, key=q_id
                )
                answers[q_id] = answer
            else:
                # Fallback for unknown types (should not happen with current questions)
                st.warning(
                    f"Unknown question type '{q_type}' for question '{q_id}'. Using text input."
                )
                answer = st.text_input(label=display_text, key=q_id)
                answers[q_id] = answer

        submitted = st.form_submit_button("Submit Answers", type="primary")

    if submitted:
        # Validate answers
        validation_results = validation_service.validate_all(questions, answers)
        validation_errors = []
        for qid, result in validation_results.items():
            if not result.is_valid:
                for error in result.errors:
                    validation_errors.append(f"'{qid}': {error}")

        if validation_errors:
            st.error("Please fix the following errors:")
            for error in validation_errors:
                st.write(f"- {error}")
        else:
            # Build context
            builder = ContextBuilder()
            try:
                context = builder.build(answers)
                st.success("✅ Context Created Successfully!")
                st.session_state.context = context
                st.session_state.answers = answers
                # Reset downstream state
                st.session_state.selected_template_id = None
                st.session_state.instruction = None
                st.session_state.version = None

                # Show context summary and JSON
                with st.expander("View Context Details", expanded=False):
                    st.subheader("Context Summary")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Objective", context.objective[:50] + "..." if len(context.objective) > 50 else context.objective)
                        st.metric("Audience", context.audience)
                        st.metric("Tone", context.tone)
                    with col2:
                        st.metric("Output Format", context.output_format)
                        st.metric("Risk Level", context.risk_level)
                        st.metric("Language", context.language)
                    st.subheader("Context JSON")
                    st.json(context.model_dump())
            except ValueError as e:
                st.error(f"❌ Failed to create Context: {e}")

    # Step 2: Template Selection (only if context exists)
    if st.session_state.context is not None:
        st.header("Step 2: Select Template")
        # Initialize container if needed
        if st.session_state.container is None:
            st.session_state.container = get_container()
        container = st.session_state.container

        # Load templates
        template_service = container.template_service
        templates = template_service.get_all()
        if not templates:
            st.warning("No templates available.")
        else:
            # Create a mapping from template name to template object
            template_options = {t.name: t for t in templates}
            template_names = list(template_options.keys())

            # Determine current selection
            current_index = 0
            if (
                st.session_state.selected_template_id is not None
                and any(t.id == st.session_state.selected_template_id for t in templates)
            ):
                # Find the index of the selected template by id
                selected_name = next(
                    t.name for t in templates if t.id == st.session_state.selected_template_id
                )
                current_index = template_names.index(selected_name)

            selected_template_name = st.selectbox(
                "Choose a template for instruction generation:",
                options=template_names,
                index=current_index,
                key="template_selectbox",
            )
            if selected_template_name:
                selected_template = template_options[selected_template_name]
                st.session_state.selected_template_id = selected_template.id

                # Show template details
                with st.expander("View Template Details", expanded=False):
                    st.subheader(f"Template: {selected_template.name}")
                    st.write(selected_template.description)
                    st.write(f"**Category:** {selected_template.category}")
                    st.write(f"**Version:** {selected_template.version}")
                    st.write("**Template Text:**")
                    st.code(selected_template.template_text, language=None)
                    st.write("**Placeholders:**", ", ".join(selected_template.placeholders))

        # Step 3: Generate Instruction
        if st.session_state.selected_template_id is not None:
            st.header("Step 3: Generate Instruction")
            
            # Generate instruction if not already generated
            if st.session_state.instruction is None:
                if st.button("Generate Instruction", type="primary"):
                    instruction_builder = container.instruction_builder
                    try:
                        instruction = instruction_builder.build(
                            st.session_state.selected_template_id, st.session_state.context
                        )
                        st.session_state.instruction = instruction
                        st.success("✅ Instruction Generated Successfully!")

                        # Display instruction and download button
                        with st.expander("View Generated Instruction", expanded=True):
                            st.subheader("Generated Instruction")
                            st.code(instruction.assembled_instruction, language=None)
                            # Download button
                            st.download_button(
                                label="Download Instruction",
                                data=instruction.assembled_instruction,
                                file_name="instruction.txt",
                                mime="text/plain",
                            )
                    except Exception as e:
                        st.error(f"❌ Failed to generate instruction: {e}")
            else:
                # Show existing instruction
                st.success("✅ Instruction Already Generated!")
                with st.expander("View Generated Instruction", expanded=True):
                    st.subheader("Generated Instruction")
                    st.code(st.session_state.instruction.assembled_instruction, language=None)
                    # Download button
                    st.download_button(
                        label="Download Instruction",
                        data=st.session_state.instruction.assembled_instruction,
                        file_name="instruction.txt",
                        mime="text/plain",
                    )

            # Create version if instruction exists but version doesn't
            if st.session_state.instruction is not None and st.session_state.version is None:
                st.header("Step 4: Create Version")
                if st.button("Create Version", type="primary"):
                    try:
                        version_service = container.version_service
                        version = version_service.create_version(
                            instruction_id=st.session_state.instruction.id,
                            change_summary="Initial Version",
                            created_by="Streamlit Demo",
                        )
                        st.session_state.version = version
                        st.success("✅ Version Created Successfully!")

                        # Display version details
                        with st.expander("View Version Details", expanded=True):
                            st.subheader("Version Information")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Version Number", version.version_number)
                            with col2:
                                st.metric("Version ID", version.id[:8] + "...")
                            with col3:
                                st.metric("Created By", version.created_by or "N/A")
                            st.write(f"**Change Summary:** {version.change_summary}")
                    except Exception as e:
                        st.error(f"❌ Failed to create version: {e}")
            elif st.session_state.version is not None:
                # Show existing version
                st.success("✅ Version Already Created!")
                with st.expander("View Version Details", expanded=True):
                    st.subheader("Version Information")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Version Number", st.session_state.version.version_number)
                    with col2:
                        st.metric("Version ID", st.session_state.version.id[:8] + "...")
                    with col3:
                        st.metric("Created By", st.session_state.version.created_by or "N/A")
                    st.write(f"**Change Summary:** {st.session_state.version.change_summary}")

    # If context exists but no instruction generated yet, show a hint
    elif st.session_state.context is not None:
        st.info("👆 Select a template and click 'Generate Instruction' to continue.")


if __name__ == "__main__":
    main()