"""
Structured data extraction using tool_use + JSON schema with validation retry.
Domain 4, Tasks 4.3-4.4: Enforce structured output and implement validation/retry loops.

Key patterns:
- tool_use + JSON schema eliminates syntax errors (but NOT semantic errors)
- tool_choice: "any" guarantees a tool call — model cannot return conversational text
- Nullable fields prevent fabrication when source data is absent
- Retry-with-error-feedback: append validation errors to prompt for self-correction
- detected_pattern field enables false-positive analysis over time
"""

import json
import anthropic

client = anthropic.Anthropic()

EXTRACTION_TOOLS = [
    {
        "name": "extract_code_review_findings",
        "description": "Extract structured code review findings from analysis text or a review document.",
        "input_schema": {
            "type": "object",
            "properties": {
                "findings": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "file_path": {
                                "type": "string"
                            },
                            "line_number": {
                                "type": ["integer", "null"],
                                "description": "Null when line number is not determinable from source — prevents fabrication"
                            },
                            "severity": {
                                "type": "string",
                                "enum": ["error", "warning", "info", "unclear"],
                                "description": "Use 'unclear' for genuinely ambiguous severity rather than guessing"
                            },
                            "category": {
                                "type": "string",
                                "enum": ["bug", "security", "performance", "style", "other"],
                                "description": "Use 'other' + category_detail for categories outside this list"
                            },
                            "category_detail": {
                                "type": ["string", "null"],
                                "description": "Required when category is 'other' — extensible categorization"
                            },
                            "message": {
                                "type": "string"
                            },
                            "suggested_fix": {
                                "type": ["string", "null"],
                                "description": "Null when no clear fix is determinable"
                            },
                            "detected_pattern": {
                                "type": ["string", "null"],
                                "description": (
                                    "The specific code pattern that triggered this finding. "
                                    "Enables systematic analysis of false-positive patterns "
                                    "when developers dismiss findings."
                                )
                            }
                        },
                        "required": ["file_path", "severity", "category", "message"]
                    }
                },
                "calculated_total": {
                    "type": "integer",
                    "description": "Total count of findings — must equal len(findings). Enables semantic validation."
                },
                "has_blocking_issues": {
                    "type": "boolean",
                    "description": "True if any finding has severity 'error'"
                },
                "confidence": {
                    "type": "number",
                    "minimum": 0,
                    "maximum": 1,
                    "description": (
                        "Model self-reported confidence in findings quality (0.0-1.0). "
                        "Enables calibrated review routing: high-confidence findings post automatically, "
                        "low-confidence findings route to human review."
                    )
                },
                "conflict_detected": {
                    "type": "boolean",
                    "description": "True if source document contains internally inconsistent information"
                }
            },
            "required": ["findings", "calculated_total", "has_blocking_issues", "confidence"]
        }
    }
]


def validate_extraction(extracted: dict) -> list[str]:
    """
    Validate semantic correctness of the extracted data.

    tool_use with JSON schema eliminates SYNTAX errors (malformed JSON, missing braces,
    wrong types). It does NOT prevent SEMANTIC errors — these must be validated separately.
    """
    errors = []

    # Semantic check: calculated_total must match actual count
    actual_count = len(extracted.get("findings", []))
    stated_total = extracted.get("calculated_total", -1)
    if stated_total != actual_count:
        errors.append(
            f"calculated_total ({stated_total}) does not match actual findings count ({actual_count}). "
            f"Update calculated_total to {actual_count}."
        )

    # Semantic check: 'other' category must have detail
    for i, finding in enumerate(extracted.get("findings", [])):
        if finding.get("category") == "other" and not finding.get("category_detail"):
            errors.append(
                f"Finding {i} (file: {finding.get('file_path', '?')}): "
                f"category 'other' requires a non-null category_detail field."
            )

    # Semantic check: has_blocking_issues must match presence of 'error' severity findings
    has_errors = any(f.get("severity") == "error" for f in extracted.get("findings", []))
    if extracted.get("has_blocking_issues") != has_errors:
        errors.append(
            f"has_blocking_issues ({extracted.get('has_blocking_issues')}) does not match "
            f"presence of 'error' severity findings ({has_errors}). Correct this field."
        )

    return errors


def extract_with_retry(document: str, max_retries: int = 2) -> dict:
    """
    Extract structured findings with retry-with-error-feedback.

    On validation failure, appends specific error descriptions to the prompt
    so the model can self-correct. This is more effective than a bare retry.

    Retries are ineffective when required information is simply absent from the
    source document — only retry for format mismatches and structural errors.
    """
    messages = [
        {
            "role": "user",
            "content": f"Analyze this code review document and extract all findings:\n\n{document}"
        }
    ]

    last_extraction = {}

    for attempt in range(max_retries + 1):
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            tools=EXTRACTION_TOOLS,
            # "any" guarantees a tool call — model cannot return conversational text instead
            tool_choice={"type": "any"},
            messages=messages
        )

        tool_block = next(
            (b for b in response.content if b.type == "tool_use"),
            None
        )

        if not tool_block:
            if attempt < max_retries:
                messages.append({"role": "assistant", "content": response.content})
                messages.append({
                    "role": "user",
                    "content": "You must call the extract_code_review_findings tool. Please extract the findings now."
                })
                continue
            break

        last_extraction = tool_block.input
        validation_errors = validate_extraction(last_extraction)

        if not validation_errors:
            return last_extraction

        if attempt < max_retries:
            error_list = "\n".join(f"  - {e}" for e in validation_errors)
            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "type": "tool_result",
                "tool_use_id": tool_block.id,
                "content": f"Validation failed with the following errors:\n{error_list}"
            })
            messages.append({
                "role": "user",
                "content": (
                    "The extraction has validation errors. Fix them and call the tool again:\n"
                    f"{error_list}"
                )
            })

    return last_extraction


if __name__ == "__main__":
    sample = """
    Code review for auth-service PR #42:

    src/auth.py, line 15: The SQL query uses string concatenation with user input —
    this is a SQL injection vulnerability (critical).

    src/utils.py: Missing input validation on the user_id parameter passed to
    get_user_profile(). Could allow unauthorized data access.

    src/main.py line 89: The for-loop calls get_orders() on every iteration —
    N+1 query pattern causing significant performance degradation on large datasets.
    """

    result = extract_with_retry(sample)
    print(json.dumps(result, indent=2))
    print(f"\nFindings: {result.get('calculated_total', 0)}")
    print(f"Blocking: {result.get('has_blocking_issues', False)}")
    print(f"Confidence: {result.get('confidence', 0):.0%}")
