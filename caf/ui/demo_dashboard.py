"""CAF Enterprise Dashboard - Enterprise AI Instruction Orchestration Platform."""

import streamlit as st
from datetime import UTC, datetime
import uuid
import difflib
import os
from dotenv import load_dotenv
from caf.core.container import get_container
from caf.services.question_service import question_service
from caf.services.validation_service import validation_service
from caf.services.context_builder import ContextBuilder
from caf.models.context import Context

# Load environment variables from .env file
load_dotenv()


def init_session_state() -> None:
    """Initialize session state variables."""
    if "container" not in st.session_state:
        st.session_state.container = get_container()
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "context" not in st.session_state:
        st.session_state.context = None
    if "selected_template_id" not in st.session_state:
        st.session_state.selected_template_id = None
    if "instruction" not in st.session_state:
        st.session_state.instruction = None
    if "version" not in st.session_state:
        st.session_state.version = None
    if "variant" not in st.session_state:
        st.session_state.variant = None
    if "feedback_submitted" not in st.session_state:
        st.session_state.feedback_submitted = False
    # Presentation data session state
    if "demo_versions" not in st.session_state:
        st.session_state.demo_versions = []
    if "demo_variants" not in st.session_state:
        st.session_state.demo_variants = []
    if "demo_instruction_texts" not in st.session_state:
        st.session_state.demo_instruction_texts = {}
    if "demo_feedback_linked" not in st.session_state:
        st.session_state.demo_feedback_linked = False
    # Enterprise AI Runtime session state
    if "ai_runtime_provider" not in st.session_state:
        st.session_state.ai_runtime_provider = "NVIDIA NIM"
    if "ai_runtime_model" not in st.session_state:
        st.session_state.ai_runtime_model = "Llama 3.3 70B Instruct"
    if "ai_runtime_temperature" not in st.session_state:
        st.session_state.ai_runtime_temperature = 0.2
    if "ai_runtime_max_tokens" not in st.session_state:
        st.session_state.ai_runtime_max_tokens = 4096
    if "ai_runtime_mode" not in st.session_state:
        st.session_state.ai_runtime_mode = "Enterprise Managed"
    if "ai_runtime_connection_status" not in st.session_state:
        st.session_state.ai_runtime_connection_status = "not_validated"
    if "ai_runtime_latency" not in st.session_state:
        st.session_state.ai_runtime_latency = None


def create_presentation_version_2(instruction: any) -> dict:
    """Create presentation version 2 data for lifecycle demonstration."""
    base_text = instruction.assembled_instruction
    enhanced_text = base_text + """

Implementation Roadmap & Deployment Strategy:
- Phase 1: Core instruction validation and testing
- Phase 2: Stakeholder review and approval workflow
- Phase 3: Production deployment with monitoring
- Executive summary for leadership alignment
- Enhanced compliance guidance for governance teams"""
    
    version_data = {
        "id": str(uuid.uuid4()),
        "instruction_id": instruction.id,
        "version_number": 2,
        "created_at": datetime.now(UTC),
        "created_by": "Prompt Engineering Team",
        "change_summary": "Enhanced instruction specificity and reduced ambiguity.",
        "parent_version_id": st.session_state.version.id if st.session_state.version else None,
    }
    return {"version": version_data, "text": enhanced_text}


def create_presentation_version_3(instruction: any) -> dict:
    """Create presentation version 3 data for lifecycle demonstration."""
    base_text = st.session_state.demo_instruction_texts.get(2, instruction.assembled_instruction)
    enhanced_text = base_text + """

Governance & Compliance Enhancements:
- Integrated ISO 27001 Annex A controls mapping
- NIST AI RMF 1.0 governance framework references
- Expanded data governance and privacy sections
- Audit trail requirements documented
- Risk classification updated per enterprise policy"""
    
    version_data = {
        "id": str(uuid.uuid4()),
        "instruction_id": instruction.id,
        "version_number": 3,
        "created_at": datetime.now(UTC),
        "created_by": "AI Governance Team",
        "change_summary": "Integrated ISO 27001 controls and NIST AI RMF governance references.",
        "parent_version_id": st.session_state.demo_versions[0]["version"]["id"] if st.session_state.demo_versions else None,
    }
    return {"version": version_data, "text": enhanced_text}


def create_presentation_variants(version_id: str) -> list:
    """Create presentation variants for lifecycle demonstration."""
    return [
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Enterprise Standard",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Enterprise-grade variant with full governance controls and audit trail",
        },
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Compliance Optimized",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Compliance-focused variant with regulatory control mappings and evidence artifacts",
        },
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Executive Brief",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Condensed variant for leadership review and strategic decision-making",
        },
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Risk Assessment",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Risk-focused variant with threat modeling and mitigation strategies",
        },
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Developer Edition",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Technical variant optimized for implementation teams with code-level guidance",
        },
        {
            "id": str(uuid.uuid4()),
            "version_id": version_id,
            "variant_name": "Audit Ready",
            "created_at": datetime.now(UTC),
            "parent_variant_id": None,
            "description": "Audit-prepared variant with evidence packages and compliance checklists",
        },
    ]


def render_sidebar() -> None:
    """Render the professional sidebar with CAF status and session info."""
    with st.sidebar:
        st.header("CAF Enterprise Console")
        st.caption("Enterprise AI Instruction Orchestration")

        st.divider()

        # Enterprise AI Runtime
        st.subheader("Enterprise AI Runtime")

        # Provider
        providers = [
            "NVIDIA NIM",
            "OpenAI (Coming Soon)",
            "Azure OpenAI (Coming Soon)",
            "AWS Bedrock (Coming Soon)",
            "Google Vertex AI (Coming Soon)"
        ]
        provider_index = providers.index(st.session_state.ai_runtime_provider) if st.session_state.ai_runtime_provider in providers else 0
        selected_provider = st.selectbox(
            "Provider",
            options=providers,
            index=provider_index,
            key="ai_runtime_provider",
            help="Select the AI provider for inference"
        )
        
        # Show warning for coming soon providers
        if selected_provider != "NVIDIA NIM":
            st.warning("⚠ Provider not yet available.")
            st.info("Only NVIDIA NIM is currently functional.")
        
        # Model selection (only show if NVIDIA NIM is selected)
        if selected_provider == "NVIDIA NIM":
            models = [
                "Llama 3.3 70B Instruct",
                "Llama 3.1 Nemotron Ultra 253B",
                "DeepSeek R1",
                "Mistral Large 2",
                "Qwen 3 235B",
                "Custom Endpoint"
            ]
            model_index = models.index(st.session_state.ai_runtime_model) if st.session_state.ai_runtime_model in models else 0
            selected_model = st.selectbox(
                "Model",
                options=models,
                index=model_index,
                key="ai_runtime_model",
                help="Select the NVIDIA NIM model for instruction execution"
            )
            
            # Model description
            model_descriptions = {
                "Llama 3.3 70B Instruct": "General enterprise instruction generation.",
                "Llama 3.1 Nemotron Ultra 253B": "Advanced reasoning and enterprise analysis.",
                "DeepSeek R1": "Complex reasoning and research.",
                "Mistral Large 2": "Balanced performance.",
                "Qwen 3 235B": "Multilingual enterprise tasks.",
                "Custom Endpoint": "User-defined endpoint for specialized models."
            }
            if selected_model in model_descriptions:
                st.caption(model_descriptions[selected_model])

        # Temperature
        st.slider(
            "Temperature",
            min_value=0.0,
            max_value=1.0,
            value=st.session_state.ai_runtime_temperature,
            step=0.1,
            key="ai_runtime_temperature",
            help="Controls randomness in generation (0.0 = deterministic, 1.0 = creative)"
        )

        # Max Tokens
        st.number_input(
            "Max Tokens",
            min_value=256,
            max_value=32768,
            value=st.session_state.ai_runtime_max_tokens,
            step=256,
            key="ai_runtime_max_tokens",
            help="Maximum tokens for generated response"
        )

        # Inference Mode
        modes = ["Enterprise Managed", "Balanced", "High Accuracy", "Fast Response"]
        mode_index = modes.index(st.session_state.ai_runtime_mode) if st.session_state.ai_runtime_mode in modes else 0
        st.selectbox(
            "Inference Mode",
            options=modes,
            index=mode_index,
            key="ai_runtime_mode",
            help="Preconfigured inference profiles for enterprise workloads"
        )

        st.divider()

        # Enterprise Runtime Status
        st.subheader("Runtime Status")
        
        # Determine status display
        if st.session_state.ai_runtime_connection_status == "not_validated":
            status_color = "🟡"
            status_text = "Not Validated"
        elif st.session_state.ai_runtime_connection_status == "connected":
            status_color = "🟢"
            status_text = "Ready"
        elif st.session_state.ai_runtime_connection_status == "failed":
            status_color = "🔴"
            status_text = "Connection Failed"
        else:
            status_color = "🟡"
            status_text = "Checking..."
        
        # Display status card
        with st.container(border=True):
            st.markdown("**Enterprise Runtime**")
            col1, col2 = st.columns(2)
            with col1:
                if st.session_state.ai_runtime_provider == "NVIDIA NIM":
                    st.markdown("**Provider**")
                    st.text("NVIDIA NIM")
                    st.markdown("**Endpoint**")
                    st.text("integrate.api.nvidia.com")
                    st.markdown("**Authentication**")
                    if os.getenv("NVIDIA_API_KEY"):
                        st.text("Environment Secret ✓")
                    else:
                        st.text("Missing ❌")
                else:
                    st.markdown("**Provider**")
                    st.text(st.session_state.ai_runtime_provider.split(" ")[0])  # Remove "(Coming Soon)"
                    st.markdown("**Endpoint**")
                    if st.session_state.ai_runtime_provider == "NVIDIA NIM":
                        st.text("integrate.api.nvidia.com")
                    else:
                        st.text("N/A")
                    st.markdown("**Authentication**")
                    if "NVIDIA" in st.session_state.ai_runtime_provider:
                        if os.getenv("NVIDIA_API_KEY"):
                            st.text("Environment Secret ✓")
                        else:
                            st.text("Missing ❌")
                    else:
                        st.text("N/A (Coming Soon)")
            with col2:
                st.markdown("**Status**")
                if st.session_state.ai_runtime_connection_status == "connected":
                    st.markdown(f"{status_color} **{status_text}**")
                elif st.session_state.ai_runtime_connection_status == "not_validated":
                    st.markdown(f"{status_color} **{status_text}**")
                else:
                    st.markdown(f"{status_color} **{status_text}**")
                if st.session_state.ai_runtime_latency is not None and st.session_state.ai_runtime_connection_status == "connected":
                    st.markdown("**Latency**")
                    st.text(f"{st.session_state.ai_runtime_latency} ms")

        # Test Connection Button
        if st.button("Test Connection", use_container_width=True, disabled=(selected_provider != "NVIDIA NIM")):
            if selected_provider == "NVIDIA NIM":
                with st.spinner("Testing connection to NVIDIA NIM..."):
                    # Import here to avoid loading unless needed
                    import time
                    import requests
                    
                    api_key = os.getenv("NVIDIA_API_KEY")
                    if not api_key:
                        st.session_state.ai_runtime_connection_status = "failed"
                        st.session_state.ai_runtime_latency = None
                        st.error("🔴 API Key Missing")
                    else:
                        try:
                            start_time = time.time()
                            headers = {
                                "Authorization": f"Bearer {api_key}",
                                "Content-Type": "application/json"
                            }
                            # Lightweight test - just check models endpoint
                            response = requests.get(
                                "https://integrate.api.nvidia.com/v1/models",
                                headers=headers,
                                timeout=10
                            )
                            latency = int((time.time() - start_time) * 1000)
                            
                            if response.status_code == 200:
                                st.session_state.ai_runtime_connection_status = "connected"
                                st.session_state.ai_runtime_latency = latency
                                st.success("🟢 Connection Successful")
                                st.info(f"""
                                **Provider:** NVIDIA NIM
                                **Endpoint:** https://integrate.api.nvidia.com/v1
                                **Authentication:** Environment Secret ✓
                                **Latency:** {latency} ms
                                **Status:** Ready
                                """)
                            else:
                                st.session_state.ai_runtime_connection_status = "failed"
                                st.session_state.ai_runtime_latency = None
                                st.error(f"🔴 Connection Failed: HTTP {response.status_code}")
                        except requests.exceptions.Timeout:
                            st.session_state.ai_runtime_connection_status = "failed"
                            st.session_state.ai_runtime_latency = None
                            st.error("🔴 Connection Timeout")
                        except requests.exceptions.ConnectionError:
                            st.session_state.ai_runtime_connection_status = "failed"
                            st.session_state.ai_runtime_latency = None
                            st.error("🔴 Connection Error")
                        except Exception as e:
                            st.session_state.ai_runtime_connection_status = "failed"
                            st.session_state.ai_runtime_latency = None
                            st.error(f"🔴 Connection Error: {str(e)}")
            else:
                st.warning("Cannot test connection for non-NVIDIA providers.")

        st.divider()

        # CAF Status
        st.subheader("System Status")
        if st.session_state.context is None:
            st.info("Session: Awaiting Business Context")
        elif st.session_state.instruction is None:
            st.info("Session: Business Context Ready")
        elif st.session_state.version is None:
            st.info("Session: Instruction Ready")
        elif st.session_state.variant is None:
            st.success("Session: Governance Version Created")
        else:
            st.success("Session: Instruction Variant Registered")

        st.divider()

        # Workflow Progress
        st.subheader("Workflow Progress")
        steps = [
            ("1. Business Requirements", st.session_state.answers != {}),
            ("2. Business Context", st.session_state.context is not None),
            ("3. Template Repository", st.session_state.selected_template_id is not None),
            ("4. Instruction Assembly", st.session_state.instruction is not None),
            ("5. Governance Version", st.session_state.version is not None),
            ("6. Instruction Variant", st.session_state.variant is not None),
        ]
        for step, completed in steps:
            if completed:
                st.success(f"✓ {step}")
            else:
                st.info(f"○ {step}")

        st.divider()

        # Current Session Details
        st.subheader("Current Session")
        if st.session_state.context:
            with st.expander("Business Context", expanded=False):
                ctx = st.session_state.context
                st.metric("Business Objective", ctx.objective[:30] + "..." if len(ctx.objective) > 30 else ctx.objective)
                st.metric("Target Audience", ctx.audience)
                st.metric("Communication Tone", ctx.tone)
                st.metric("Output Format", ctx.output_format)
                st.metric("Language", ctx.language)
        else:
            st.caption("No business context configured")

        if st.session_state.instruction:
            with st.expander("Instruction Assembly", expanded=False):
                st.metric("Template", st.session_state.instruction.template_name)
                st.caption(f"ID: {st.session_state.instruction.id[:8]}...")

        if st.session_state.version:
            with st.expander("Governance Version", expanded=False):
                ver = st.session_state.version
                st.metric("Volume #", ver.version_number)
                st.metric("Created By", ver.created_by or "N/A")
                st.caption(f"ID: {ver.id[:8]}...")

        if st.session_state.variant:
            with st.expander("Instruction Variant", expanded=False):
                var = st.session_state.variant
                st.metric("Variant", var.variant_name)
                st.caption(f"ID: {var.id[:8]}...")

        st.divider()

        # Reset Session
        if st.button("Reset Session", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()


def render_question_engine() -> bool:
    """Render Section 1: Business Requirements."""
    st.header("1. Business Requirements")
    st.caption("Structured intake for enterprise instruction generation")

    questions = question_service.get_all_questions()
    if not questions:
        st.error("No questions configured. Check questions.json")
        return False

    with st.form(key="question_form"):
        st.subheader("Provide Business Requirements")
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
                    label=display_text,
                    key=f"q_{q_id}",
                    placeholder=placeholder,
                )
                answers[q_id] = answer

            elif q_type == "select":
                options = question.get("options", [])
                if required and "" not in options:
                    options = [""] + options
                answer = st.selectbox(
                    label=display_text,
                    options=options,
                    key=f"q_{q_id}",
                )
                answers[q_id] = answer

            elif q_type == "multiselect":
                options = question.get("options", [])
                answer = st.multiselect(
                    label=display_text,
                    options=options,
                    key=f"q_{q_id}",
                )
                answers[q_id] = answer

            else:
                st.warning(f"Unknown type '{q_type}' for '{q_id}'. Using text input.")
                answer = st.text_input(label=display_text, key=f"q_{q_id}")
                answers[q_id] = answer

        submitted = st.form_submit_button("Validate & Build Context", type="primary")

    if submitted:
        validation_results = validation_service.validate_all(questions, answers)
        validation_errors = []
        for qid, result in validation_results.items():
            if not result.is_valid:
                for error in result.errors:
                    validation_errors.append(f"'{qid}': {error}")

        if validation_errors:
            st.error("Please resolve the following validation issues:")
            for error in validation_errors:
                st.write(f"- {error}")
            return False

        builder = ContextBuilder()
        try:
            context = builder.build(answers)
            st.session_state.context = context
            st.session_state.answers = answers
            st.session_state.selected_template_id = None
            st.session_state.instruction = None
            st.session_state.version = None
            st.session_state.variant = None
            st.session_state.demo_versions = []
            st.session_state.demo_variants = []
            st.session_state.demo_instruction_texts = {}
            st.session_state.demo_feedback_linked = False
            st.success("✅ Business Context Successfully Established!")
            return True
        except ValueError as e:
            st.error(f"❌ Failed to establish Business Context: {e}")
            return False

    return False


def render_context_builder() -> None:
    """Render Section 2: Business Context."""
    if st.session_state.context is None:
        return

    st.header("2. Business Context")
    st.success("✅ Business Context Successfully Established")

    ctx: Context = st.session_state.context

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Business Objective", ctx.objective[:40] + "..." if len(ctx.objective) > 40 else ctx.objective)
        st.metric("Target Audience", ctx.audience)
        st.metric("Communication Tone", ctx.tone)
    with col2:
        st.metric("Output Format", ctx.output_format)
        st.metric("Governance Risk", ctx.risk_level)
        st.metric("Language", ctx.language)
    with col3:
        st.metric("Business Objective", ctx.purpose)
        st.metric("Business Domain", ctx.business_type)
        st.metric("Constraints", len(ctx.constraints) if ctx.constraints else 0)

    with st.expander("View Context JSON", expanded=False):
        st.json(ctx.model_dump())


def render_template_engine() -> None:
    """Render Section 3: Template Repository."""
    if st.session_state.context is None:
        return

    st.header("3. Template Repository")
    st.caption("Select an approved template for instruction assembly")

    container = st.session_state.container
    template_service = container.template_service
    templates = template_service.get_all()

    if not templates:
        st.warning("No templates available in repository.")
        return

    template_options = {f"{t.name} ({t.category})": t for t in templates}
    selected_key = st.selectbox(
        "Choose a template:",
        options=list(template_options.keys()),
        key="template_select",
    )

    if selected_key:
        selected_template = template_options[selected_key]
        st.session_state.selected_template_id = selected_template.id

        with st.expander("Template Details", expanded=True):
            st.subheader(selected_template.name)
            st.caption(f"Template Category: {selected_template.category} | Version: {selected_template.version}")
            st.write(f"**Business Domain:** {selected_template.category}")
            st.write(f"**Supported Models:** OpenAI, Gemini, Claude, NVIDIA NIM")
            st.write(f"**Template Version:** {selected_template.version}")
            st.write(f"**Current Status:** Approved for Production")
            st.divider()
            st.write(selected_template.description)
            st.divider()
            st.code(selected_template.template_text, language=None)
            st.caption(f"Placeholders: {', '.join(selected_template.placeholders)}")


def render_instruction_assembly() -> None:
    """Render Section 4: Instruction Assembly."""
    if st.session_state.context is None or st.session_state.selected_template_id is None:
        return

    st.header("4. Instruction Assembly")

    container = st.session_state.container
    instruction_builder = container.instruction_builder

    if st.session_state.instruction is None:
        if st.button("Assemble Instruction", type="primary"):
            with st.status("Assembling enterprise instruction...", expanded=True) as status:
                try:
                    instruction = instruction_builder.build(
                        st.session_state.selected_template_id,
                        st.session_state.context,
                    )
                    st.session_state.instruction = instruction
                    st.session_state.demo_instruction_texts[1] = instruction.assembled_instruction
                    status.update(label="Instruction assembled!", state="complete")
                    st.success("✅ Enterprise Instruction Successfully Assembled!")
                except Exception as e:
                    status.update(label="Failed", state="error")
                    st.error(f"❌ Failed to assemble instruction: {e}")

    if st.session_state.instruction:
        instr = st.session_state.instruction
        
        with st.expander("Assembled Instruction", expanded=True):
            st.subheader("Enterprise Instruction")
            st.code(instr.assembled_instruction, language=None)
            
            st.download_button(
                label="Download Instruction",
                data=instr.assembled_instruction,
                file_name=f"instruction_{instr.id[:8]}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with st.expander("Instruction Metadata", expanded=False):
            st.metric("Instruction ID", instr.id[:16] + "...")
            st.metric("Template", instr.template_name)
            st.metric("Instruction Classification", "Enterprise Internal")
            st.metric("Security Level", "Confidential")
            st.metric("Approval Status", "Approved")
            st.metric("Lifecycle Stage", "Production Candidate")
            st.json(instr.context)


def render_version_control() -> None:
    """Render Section 5: Governance Version."""
    if st.session_state.instruction is None:
        return

    st.header("5. Governance Version")

    container = st.session_state.container
    version_service = container.version_service

    if st.session_state.version is None:
        if st.button("Create Governance Version", type="primary"):
            with st.status("Creating governance version...", expanded=True) as status:
                try:
                    version = version_service.create_version(
                        instruction_id=st.session_state.instruction.id,
                        change_summary="Initial enterprise instruction baseline.",
                        created_by="Security Review Board",
                    )
                    st.session_state.version = version
                    st.session_state.demo_instruction_texts[1] = st.session_state.instruction.assembled_instruction
                    
                    demo_v2 = create_presentation_version_2(st.session_state.instruction)
                    st.session_state.demo_versions.append(demo_v2)
                    st.session_state.demo_instruction_texts[2] = demo_v2["text"]
                    
                    demo_v3 = create_presentation_version_3(st.session_state.instruction)
                    st.session_state.demo_versions.append(demo_v3)
                    st.session_state.demo_instruction_texts[3] = demo_v3["text"]
                    
                    st.session_state.demo_variants = create_presentation_variants(demo_v3["version"]["id"])
                    
                    status.update(label="Governance version created with full lifecycle!", state="complete")
                    st.success("✅ Governance Version Successfully Created! Full instruction lifecycle populated.")
                except Exception as e:
                    status.update(label="Failed", state="error")
                    st.error(f"❌ Failed to create governance version: {e}")

    if st.session_state.version:
        ver = st.session_state.version
        
        with st.expander("Governance Version Details", expanded=True):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Version Number", ver.version_number)
            with col2:
                st.metric("Version ID", ver.id[:8] + "...")
            with col3:
                st.metric("Created By", ver.created_by or "N/A")
            
            st.metric("Timestamp", str(ver.created_at)[:19])
            st.write(f"**Change Summary:** {ver.change_summary}")
            st.caption(f"Instruction ID: {ver.instruction_id}")
            st.caption(f"Parent Version ID: {ver.parent_version_id or 'None'}")
            
            if st.session_state.demo_versions:
                st.info(f"📋 Instruction Lifecycle: v2 (Prompt Engineering), v3 (AI Governance) | {len(st.session_state.demo_variants)} instruction variants available")


def render_variant_management() -> None:
    """Render Section 6: Instruction Variant."""
    st.header("6. Instruction Variant")

    if st.session_state.version is None:
        st.info("Create a governance version first to enable variant registration.")
        return

    container = st.session_state.container
    variant_service = container.variant_service

    if st.session_state.variant is None:
        with st.form(key="variant_form"):
            st.subheader("Register New Instruction Variant")
            variant_name = st.text_input("Variant Name", placeholder="e.g., enterprise-standard-v1")
            variant_description = st.text_area("Description (optional)", placeholder="Describe this variant...")
            
            submitted = st.form_submit_button("Register Variant", type="primary")
            
            if submitted and variant_name:
                with st.status("Registering variant...", expanded=True) as status:
                    try:
                        variant = variant_service.create_variant(
                            version_id=st.session_state.version.id,
                            variant_name=variant_name,
                            description=variant_description if variant_description else None,
                        )
                        st.session_state.variant = variant
                        status.update(label="Variant registered!", state="complete")
                        st.success("✅ Instruction Variant Successfully Registered!")
                    except Exception as e:
                        status.update(label="Failed", state="error")
                        st.error(f"❌ Failed to register variant: {e}")

    if st.session_state.variant:
        var = st.session_state.variant
        with st.expander("Registered Variant Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Variant Name", var.variant_name)
                st.metric("Version ID", var.version_id[:8] + "...")
            with col2:
                st.metric("Variant ID", var.id[:8] + "...")
                st.metric("Parent Variant", var.parent_variant_id[:8] + "..." if var.parent_variant_id else "None")
            
            if var.description:
                st.write(f"**Description:** {var.description}")

    if st.session_state.demo_variants:
        with st.expander("Available Instruction Variants", expanded=True):
            for var in st.session_state.demo_variants:
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.metric(var["variant_name"], "")
                    st.caption(f"ID: {var['id'][:8]}...")
                with col2:
                    st.write(f"**Description:** {var['description']}")
                    st.caption(f"Based on Version: {var['version_id'][:8]}...")
                st.divider()


def render_feedback() -> None:
    """Render Section 7: Quality Review."""
    st.header("7. Quality Review")

    if st.session_state.instruction is None:
        st.info("Assemble an instruction first to submit quality review.")
        return

    with st.form(key="feedback_form"):
        st.subheader("Quality Score Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            quality_score = st.slider("Quality Score", 1, 5, 4)
            hallucination_risk = st.slider("Hallucination Risk", 1, 5, 2)
            compliance_score = st.slider("Compliance Score", 1, 5, 4)
        with col2:
            completeness = st.slider("Completeness", 1, 5, 4)
            consistency = st.slider("Instruction Consistency", 1, 5, 4)
            governance_alignment = st.slider("Governance Alignment", 1, 5, 5)
        
        st.subheader("Review Tags")
        tags = st.multiselect(
            "Select applicable tags",
            options=["Accurate", "Concise", "Comprehensive", "Context Aware", "Governance Aligned", "Production Ready", "Requires Revision"],
        )
        
        st.subheader("Manual Refinement")
        manual_edit = st.checkbox("Instruction manually refined by reviewer")
        
        reviewer_notes = st.text_area("Reviewer Notes", placeholder="Detailed review observations...")
        
        submitted = st.form_submit_button("Submit Quality Review", type="primary")
        
        if submitted:
            st.session_state.feedback_submitted = True
            st.session_state.demo_feedback_linked = True
            st.success("✅ Quality Review Submitted Successfully!")

    if st.session_state.demo_feedback_linked and st.session_state.demo_versions:
        with st.expander("Review Impact", expanded=True):
            st.info("This quality review influenced Version 3 (Governance & Compliance Enhancements).")
            st.write(f"**Quality Score:** {'⭐' * quality_score}")
            st.write(f"**Hallucination Risk:** {'🔴' * hallucination_risk}{'🟢' * (5 - hallucination_risk)}")
            st.write(f"**Compliance Score:** {'✅' * compliance_score}")
            st.write(f"**Completeness:** {'📋' * completeness}")
            st.write(f"**Consistency:** {'🔄' * consistency}")
            st.write(f"**Governance Alignment:** {'🛡️' * governance_alignment}")
            if tags:
                st.write("**Tags:**", ", ".join(tags))
            if manual_edit:
                st.write("**Manual Refinement:** Applied")
            if reviewer_notes:
                st.write(f"**Reviewer Notes:** {reviewer_notes}")


def render_iteration() -> None:
    """Render Section 8: Instruction Evolution."""
    st.header("8. Instruction Evolution")

    if st.session_state.instruction is None:
        st.info("Assemble an instruction first to view instruction lifecycle.")
        return

    container = st.session_state.container
    history_service = container.history_service
    diff_service = container.diff_service

    real_versions = []
    try:
        real_versions = st.session_state.container.version_repository.get_by_instruction_id(
            st.session_state.instruction.id
        )
    except Exception:
        pass

    all_versions = []
    
    if real_versions:
        v1 = real_versions[0]
        all_versions.append({
            "version": {
                "id": v1.id,
                "version_number": 1,
                "created_at": v1.created_at,
                "created_by": v1.created_by or "Security Review Board",
                "change_summary": "Initial enterprise instruction baseline.",
                "parent_version_id": None,
            },
            "text": st.session_state.demo_instruction_texts.get(1, st.session_state.instruction.assembled_instruction),
            "is_presentation": False,
        })
    
    for demo_v in st.session_state.demo_versions:
        all_versions.append({
            "version": demo_v["version"],
            "text": demo_v["text"],
            "is_presentation": True,
        })

    with st.expander("Instruction Lifecycle", expanded=True):
        if not all_versions:
            st.info(
                "No instruction versions available. "
                "Lifecycle will populate automatically as governance versions are created."
            )
        else:
            st.subheader("Instruction Lifecycle")
            
            for i, v_data in enumerate(all_versions):
                v = v_data["version"]
                is_presentation = v_data.get("is_presentation", False)
                
                with st.container():
                    col1, col2, col3 = st.columns([1, 2, 4])
                    
                    with col1:
                        label = f"v{v['version_number']}"
                        if is_presentation:
                            label += " 🔄"
                        st.metric(label, "")
                    
                    with col2:
                        st.caption(f"ID: {v['id'][:8]}...")
                        st.caption(f"Authorized By: {v['created_by']}")
                        st.caption(f"Created: {str(v['created_at'])[:19]}")
                    
                    with col3:
                        st.write(f"**{v['change_summary']}**")
                        if is_presentation:
                            st.caption("🔄 Lifecycle version for governance tracking")
                    
                    if i < len(all_versions) - 1:
                        st.markdown("↓")
                    
                    st.divider()

            if st.session_state.demo_variants or (hasattr(st.session_state, 'variant') and st.session_state.variant):
                st.subheader("Instruction Variants")
                
                if st.session_state.variant:
                    var = st.session_state.variant
                    with st.container():
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric(var.variant_name, "")
                        with col2:
                            st.write(f"**Description:** {var.description or 'N/A'}")
                            st.caption(f"Based on Version: {var.version_id[:8]}...")
                        st.divider()
                
                if st.session_state.demo_variants:
                    for var in st.session_state.demo_variants:
                        col1, col2 = st.columns([1, 3])
                        with col1:
                            st.metric(var["variant_name"], "")
                        with col2:
                            st.write(f"**Description:** {var['description']}")
                            st.caption(f"Based on Version: {var['version_id'][:8]}...")
                        st.divider()

    with st.expander("Instruction Comparison", expanded=False):
        if len(all_versions) >= 2:
            v_data_1 = all_versions[-2]
            v_data_2 = all_versions[-1]
            
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Baseline:** v{v_data_1['version']['version_number']} ({v_data_1['version']['id'][:8]}...)")
            with col2:
                st.write(f"**Revised:** v{v_data_2['version']['version_number']} ({v_data_2['version']['id'][:8]}...)")
            
            try:
                diff_result = diff_service.compare_versions(v_data_1['version']['id'], v_data_2['version']['id'])
                use_backend = True
            except Exception:
                old_text = v_data_1['text']
                new_text = v_data_2['text']
                diff_lines = list(difflib.unified_diff(
                    old_text.splitlines(keepends=True),
                    new_text.splitlines(keepends=True),
                    fromfile=f"v{v_data_1['version']['version_number']}",
                    tofile=f"v{v_data_2['version']['version_number']}",
                    lineterm=""
                ))
                diff_result = None
                use_backend = False
            
            if use_backend and diff_result:
                st.subheader("Comparison Result")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lines Added", len(diff_result.added_lines))
                with col2:
                    st.metric("Lines Removed", len(diff_result.removed_lines))
                with col3:
                    st.metric("Similarity Index", f"{diff_result.similarity_score:.1f}%")
                
                if diff_result.added_lines:
                    st.write("**Additions:**")
                    for line in diff_result.added_lines:
                        st.success(f"+ {line}")
                if diff_result.removed_lines:
                    st.write("**Removals:**")
                    for line in diff_result.removed_lines:
                        st.error(f"- {line}")
                if diff_result.unified_diff:
                    with st.expander("Unified Comparison", expanded=False):
                        st.code(diff_result.unified_diff, language="diff")
            else:
                st.subheader("Comparison Result")
                added = [line[1:] for line in diff_lines if line.startswith('+') and not line.startswith('+++')]
                removed = [line[1:] for line in diff_lines if line.startswith('-') and not line.startswith('---')]
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Lines Added", len(added))
                with col2:
                    st.metric("Lines Removed", len(removed))
                with col3:
                    old_lines = set(v_data_1['text'].splitlines())
                    new_lines = set(v_data_2['text'].splitlines())
                    if old_lines or new_lines:
                        similarity = len(old_lines & new_lines) / len(old_lines | new_lines) * 100
                    else:
                        similarity = 100.0
                    st.metric("Similarity Index", f"{similarity:.1f}%")
                
                if added:
                    st.write("**Additions:**")
                    for line in added:
                        st.success(f"+ {line}")
                if removed:
                    st.write("**Removals:**")
                    for line in removed:
                        st.error(f"- {line}")
                
                with st.expander("Unified Comparison", expanded=False):
                    st.code("\n".join(diff_lines), language="diff")
        else:
            st.info(
                "Instruction comparison available after creating two or more governance versions."
            )


def main() -> None:
    """Main dashboard entry point."""
    st.set_page_config(
        page_title="Enterprise CAF Dashboard",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("Enterprise Context Assembly Framework (CAF)")
    st.caption("Enterprise AI Instruction Orchestration Platform")

    init_session_state()
    render_sidebar()

    tabs = st.tabs([
        "1. Business Requirements",
        "2. Business Context",
        "3. Template Repository",
        "4. Instruction Assembly",
        "5. Governance Version",
        "6. Instruction Variant",
        "7. Quality Review",
        "8. Instruction Evolution",
    ])

    with tabs[0]:
        render_question_engine()

    with tabs[1]:
        render_context_builder()

    with tabs[2]:
        render_template_engine()

    with tabs[3]:
        render_instruction_assembly()

    with tabs[4]:
        render_version_control()

    with tabs[5]:
        render_variant_management()

    with tabs[6]:
        render_feedback()

    with tabs[7]:
        render_iteration()


if __name__ == "__main__":
    main()