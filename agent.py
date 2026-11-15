
import json

from langchain_ollama import ChatOllama
from prompts import ANALYSIS_PROMPT, TEST_CASE_PROMPT
from test_case_generator import (
    parse_json_response,
    validate_analysis,
    validate_test_cases
)

MODEL_NAME = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434"


def get_llm():
    return ChatOllama(
        model=MODEL_NAME,
        base_url=OLLAMA_URL,
        temperature=0.2,
        format="json",
        timeout=180
    )


def generate_from_requirement(requirement, count=7):

    if not requirement or not requirement.strip():
        raise ValueError("Requirement cannot be empty.")

    llm = get_llm()

    analysis_prompt = ANALYSIS_PROMPT.format(
        requirement=requirement
    )

    analysis_response = llm.invoke(analysis_prompt).content

    analysis_data = parse_json_response(analysis_response)
    analysis = validate_analysis(analysis_data)

    generation_prompt = TEST_CASE_PROMPT.format(
        requirement=requirement,
        analysis=json.dumps(analysis, ensure_ascii=False),
        count=count
    )

    generation_response = llm.invoke(generation_prompt).content

    generated_data = parse_json_response(generation_response)

    cases = validate_test_cases(generated_data, count)

    if not cases:
        raise ValueError("No valid test cases generated.")

    return analysis, cases
