
# AI Test Case Generator Agent

## Project Overview

AI Test Case Generator Agent is a local AI-powered software testing application.

It converts plain-English software requirements into structured manual test cases.

## Features

- Requirement understanding
- Positive test scenarios
- Negative test scenarios
- Edge-case scenarios
- Test steps and test data
- Expected results
- High, Medium and Low priorities
- Edit and delete test cases
- SQLite history
- CSV export
- Error handling

## Technology Stack

- Python
- Streamlit
- Ollama
- Qwen2.5:3b
- LangChain
- SQLite
- Pandas

## Installation

Install dependencies:

    python -m pip install -r requirements.txt

Download the local model:

    ollama pull qwen2.5:3b

Run the application:

    python -m streamlit run app.py

## Project Structure

    app.py
    agent.py
    test_case_generator.py
    prompts.py
    database.py
    export_utils.py
    requirements.txt
    .gitignore
    README.md

## Important Note

AI-generated test cases must be reviewed by a human tester before actual use.
