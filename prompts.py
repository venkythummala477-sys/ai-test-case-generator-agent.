
ANALYSIS_PROMPT = """
You are an expert software testing analyst.

Analyze the following software requirement.

Identify:
1. Main feature
2. Testing purpose
3. Important conditions
4. Positive scenarios
5. Negative scenarios
6. Edge cases
7. Missing information and assumptions

Do not invent application rules.

Return ONLY valid JSON:

{{
    "feature": "Feature name",
    "testing_purpose": "Testing purpose",
    "important_conditions": ["condition 1"],
    "scenario_categories": [
        "Positive",
        "Negative",
        "Edge Case"
    ],
    "assumptions": []
}}

Requirement:
{requirement}
"""


TEST_CASE_PROMPT = """
You are a professional manual software tester.

Generate exactly {count} test cases from the given requirement.

Requirement:
{requirement}

Analysis:
{analysis}

Return ONLY valid JSON in this format:

{{
    "test_cases": [
        {{
            "title": "Valid login test",
            "scenario_type": "Positive",
            "preconditions": "User account exists",
            "steps": [
                "Open login page",
                "Enter valid email",
                "Enter valid password",
                "Click login"
            ],
            "test_data": "Email: user@example.com, Password: Test@123",
            "expected_result": "User should login successfully",
            "priority": "High"
        }}
    ]
}}

Rules:

- Include Positive, Negative and Edge Case scenarios where applicable.
- Use only the information in the requirement.
- Do not invent business rules.
- Mention assumptions clearly.
- Steps must be an array.
- Expected results must be clear.
- Priority must be High, Medium or Low.
- Avoid duplicate test cases.
- Generate exactly {count} test cases.
"""
