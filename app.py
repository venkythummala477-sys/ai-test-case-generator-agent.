
import streamlit as st
import pandas as pd

from agent import generate_from_requirement
from database import init_db, save_run, get_runs, get_run, delete_run
from export_utils import export_csv

st.set_page_config(
    page_title="AI Test Case Generator Agent",
    page_icon="🧪",
    layout="wide"
)

init_db()

if "test_cases" not in st.session_state:
    st.session_state.test_cases = []

if "analysis" not in st.session_state:
    st.session_state.analysis = {}

if "requirement" not in st.session_state:
    st.session_state.requirement = ""

st.title("🧪 AI Test Case Generator Agent")
st.caption("Generate, review, edit and export software test cases using local AI.")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Generate Test Cases", "History", "How It Works"]
)

if page == "Dashboard":
    runs = get_runs()

    col1, col2, col3 = st.columns(3)
    col1.metric("Saved Runs", len(runs))
    col2.metric("Saved Test Cases", sum(r["case_count"] for r in runs))
    col3.metric("AI Model", "Qwen2.5:3b")

    st.subheader("Welcome")
    st.write(
        "Enter a software requirement and let the AI agent "
        "generate positive, negative and edge-case test scenarios."
    )

    st.info("Select Generate Test Cases from the sidebar to begin.")

elif page == "Generate Test Cases":
    st.header("Generate Test Cases")

    requirement = st.text_area(
        "Enter Software Requirement",
        value=st.session_state.requirement,
        height=160,
        placeholder="Example: A user should be able to login using email and password."
    )

    count = st.slider("Number of test cases", 3, 15, 7)

    if st.button("Generate Test Cases", type="primary"):
        if not requirement.strip():
            st.warning("Please enter a requirement.")
        elif len(requirement.strip()) < 15:
            st.warning("Please enter a more detailed requirement.")
        else:
            try:
                with st.spinner("AI agent is analyzing and generating test cases..."):
                    analysis, cases = generate_from_requirement(
                        requirement, count
                    )

                st.session_state.requirement = requirement
                st.session_state.analysis = analysis
                st.session_state.test_cases = cases

                st.success(f"{len(cases)} test cases generated successfully!")

            except Exception as e:
                st.error(f"Generation failed: {e}")
                st.info(
                    "Make sure Ollama is running and qwen2.5:3b is installed."
                )

    if st.session_state.test_cases:
        st.divider()

        st.subheader("Requirement Analysis")
        analysis = st.session_state.analysis

        st.write("**Feature:**", analysis.get("feature", ""))
        st.write("**Testing Purpose:**", analysis.get("testing_purpose", ""))
        st.write(
            "**Important Conditions:**",
            ", ".join(analysis.get("important_conditions", []))
        )
        st.write(
            "**Scenario Categories:**",
            ", ".join(analysis.get("scenario_categories", []))
        )

        if analysis.get("assumptions"):
            st.warning(
                "Assumptions: " + "; ".join(analysis["assumptions"])
            )

        st.subheader("Generated Test Cases")

        df = pd.DataFrame(st.session_state.test_cases)

        edited_df = st.data_editor(
            df,
            use_container_width=True,
            hide_index=True,
            num_rows="dynamic",
            key="test_case_editor"
        )

        edited_cases = edited_df.fillna("").to_dict("records")

        for index, case in enumerate(edited_cases, start=1):
            case["id"] = f"TC-{index:03d}"

        st.session_state.test_cases = edited_cases

        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("Save to History", type="primary"):
                run_id = save_run(
                    st.session_state.requirement,
                    st.session_state.analysis,
                    st.session_state.test_cases
                )
                st.success(f"Saved successfully. Run ID: {run_id}")

        with col2:
            csv_data = export_csv(st.session_state.test_cases)
            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="test_cases.csv",
                mime="text/csv"
            )

        with col3:
            delete_ids = st.multiselect(
                "Delete test cases",
                [case["id"] for case in st.session_state.test_cases]
            )

            if st.button("Delete Selected"):
                st.session_state.test_cases = [
                    case for case in st.session_state.test_cases
                    if case["id"] not in delete_ids
                ]
                st.rerun()

elif page == "History":
    st.header("Saved Test Case History")

    runs = get_runs()

    if not runs:
        st.info("No saved history available.")
    else:
        options = {
            f"Run #{r['id']} | {r['created_at']} | {r['case_count']} cases": r["id"]
            for r in runs
        }

        selected = st.selectbox("Select saved run", list(options.keys()))
        run = get_run(options[selected])

        if run:
            st.subheader("Requirement")
            st.write(run["requirement"])

            st.subheader("Test Cases")
            st.dataframe(
                pd.DataFrame(run["cases"]),
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "Download Saved CSV",
                export_csv(run["cases"]),
                file_name=f"saved_test_cases_{run['id']}.csv",
                mime="text/csv"
            )

            if st.button("Delete Saved Run"):
                delete_run(run["id"])
                st.success("History deleted.")
                st.rerun()

elif page == "How It Works":
    st.header("How It Works")

    st.markdown("""
    1. User enters a software requirement.
    2. AI agent analyzes the requirement.
    3. Agent identifies positive, negative and edge scenarios.
    4. Local LLM generates structured test cases.
    5. Python validates the generated JSON.
    6. User edits or deletes test cases.
    7. SQLite saves previous results.
    8. Pandas exports test cases into CSV.

    **Technology Stack**

    - Python
    - Streamlit
    - Ollama
    - Qwen2.5:3b
    - LangChain
    - SQLite
    - Pandas
    """)
