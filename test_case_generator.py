
import json
import re

REQUIRED_FIELDS = [
    "title",
    "scenario_type",
    "preconditions",
    "steps",
    "test_data",
    "expected_result",
    "priority"
]

VALID_SCENARIOS = {
    "Positive",
    "Negative",
    "Edge Case"
}

VALID_PRIORITIES = {
    "High",
    "Medium",
    "Low"
}


def parse_json_response(response):

    if isinstance(response, dict):
        return response

    if not isinstance(response, str):
        raise ValueError("Invalid AI response.")

    response = response.strip()

    response = re.sub(
        r"^```(?:json)?\s*",
        "",
        response,
        flags=re.IGNORECASE
    )

    response = re.sub(r"\s*```$", "", response)

    try:
        return json.loads(response)

    except json.JSONDecodeError:
        start = response.find("{")
        end = response.rfind("}")

        if start >= 0 and end > start:
            try:
                return json.loads(response[start:end + 1])
            except json.JSONDecodeError:
                pass

        raise ValueError("AI returned invalid JSON.")


def validate_analysis(data):

    if not isinstance(data, dict):
        raise ValueError("Invalid requirement analysis.")

    return {
        "feature": str(data.get("feature", "Not specified")),
        "testing_purpose": str(
            data.get("testing_purpose", "Verify the requirement")
        ),
        "important_conditions": _string_list(
            data.get("important_conditions", [])
        ),
        "scenario_categories": _string_list(
            data.get("scenario_categories", [])
        ),
        "assumptions": _string_list(
            data.get("assumptions", [])
        )
    }


def _string_list(value):

    if isinstance(value, list):
        return [
            str(item).strip()
            for item in value
            if str(item).strip()
        ]

    if isinstance(value, str) and value.strip():
        return [value.strip()]

    return []


def validate_test_cases(data, requested_count=7):

    if isinstance(data, list):
        raw_cases = data

    elif isinstance(data, dict):
        raw_cases = data.get("test_cases", [])

    else:
        raise ValueError("Invalid test case response.")

    if not isinstance(raw_cases, list):
        raise ValueError("Test cases must be a list.")

    valid_cases = []
    seen_titles = set()

    for item in raw_cases:

        if not isinstance(item, dict):
            continue

        if any(field not in item for field in REQUIRED_FIELDS):
            continue

        title = str(item["title"]).strip()

        if not title or title.lower() in seen_titles:
            continue

        scenario = str(item["scenario_type"]).strip()

        if scenario not in VALID_SCENARIOS:
            continue

        priority = str(item["priority"]).strip()

        if priority not in VALID_PRIORITIES:
            continue

        steps = item["steps"]

        if isinstance(steps, list):
            steps = [
                str(step).strip()
                for step in steps
                if str(step).strip()
            ]

        elif isinstance(steps, str):
            steps = [
                step.strip()
                for step in re.split(r"[\n|]+", steps)
                if step.strip()
            ]

        else:
            continue

        if not steps:
            continue

        seen_titles.add(title.lower())

        valid_cases.append({
            "id": f"TC-{len(valid_cases) + 1:03d}",
            "title": title,
            "scenario_type": scenario,
            "preconditions": str(item["preconditions"]).strip(),
            "steps": " | ".join(steps),
            "test_data": str(item["test_data"]).strip(),
            "expected_result": str(item["expected_result"]).strip(),
            "priority": priority
        })

        if len(valid_cases) >= requested_count:
            break

    return valid_cases
