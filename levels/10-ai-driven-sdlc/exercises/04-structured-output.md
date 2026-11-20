# Exercise 4 — Structured Output & Prompt Engineering
### Domain 4, Tasks 4.1–4.4 · Exam weight: 20%

> Reference implementation: [`../examples/structured-output.py`](../examples/structured-output.py)

---

## Learning Objectives

- Enforce structured output using `tool_use` with JSON schemas
- Choose the correct `tool_choice` option for each scenario
- Design nullable fields to prevent model fabrication
- Implement retry-with-error-feedback for semantic validation failures
- Apply explicit criteria and few-shot prompting to reduce false positives

---

## Concept Summary

### tool_choice Options

| Value | Model behavior | Use when |
|-------|---------------|----------|
| `{"type": "auto"}` | May call a tool OR return text | Tool call is optional |
| `{"type": "any"}` | Must call a tool (any available) | Structured output required; document type unknown |
| `{"type": "tool", "name": "X"}` | Must call tool X specifically | Sequenced pipeline (X must run before Y) |

### What tool_use Guarantees vs What It Doesn't

**Eliminates (syntax errors):** malformed JSON, wrong types, missing required fields.

**Does NOT prevent (semantic errors):**
- `calculated_total: 3` when there are actually 5 findings
- Values placed in the wrong field
- Fabricated values in required fields when source data is absent

→ Semantic validation must be done in application code (see `validate_extraction()` in the reference).

### Nullable Fields for Reliability

```json
{
  "line_number": {"type": ["integer", "null"]},
  "suggested_fix": {"type": ["string", "null"]}
}
```

When a field may not be determinable from the source (e.g., line number not mentioned), mark it nullable. This prevents the model from inventing a plausible-but-wrong value to satisfy a required field.

### Retry-with-Error-Feedback

Effective for: format mismatches, structural errors, wrong field placement.

NOT effective for: information that is simply absent from the source document. If the document doesn't contain a line number, retrying won't produce one — it will hallucinate.

---

## Exercises

### 4.1 — tool_choice Selection

Choose the correct `tool_choice` for each scenario:

**Scenario A**: You have one extraction tool and want guaranteed structured output. No text response needed.

**Scenario B**: You have three extraction tools (`extract_invoice`, `extract_receipt`, `extract_purchase_order`). You don't know which document type you're processing.

**Scenario C**: Your pipeline runs `extract_metadata` first, then `enrich_with_taxonomy`. The enrichment step must never run before metadata extraction.

Write the `tool_choice` value for each scenario.

---

### 4.2 — Schema Design

Design a JSON schema for extracting invoice data from unstructured documents:

**Requirements:**
- Handle invoices that may be missing: line items, tax amount, discount, payment terms
- Prevent fabrication of monetary amounts not present in the source
- Include a field that flags when stated total doesn't match the sum of line items
- Use extensible categorization for payment method (not all methods are pre-known)
- Include a confidence field for calibrated routing

Write the schema. For each nullable field, add a one-line comment explaining why it's nullable.

---

### 4.3 — Few-Shot Examples for Severity Classification

Your CI review pipeline classifies findings as `error`, `warning`, or `info`. Developers are dismissing `warning`-level findings because severity is inconsistent — performance issues sometimes appear as `error`, sometimes as `warning`.

Write **3 few-shot examples** to include in the extraction prompt that demonstrate consistent severity classification:

1. A confirmed SQL injection vulnerability
2. An N+1 query pattern in a non-critical background job
3. A missing database index on a column used in 80% of queries

Each example should show:
- The code pattern found (brief description)
- The correct severity
- A one-sentence justification

---

### 4.4 — Analyze the Retry Logic

Open `../examples/structured-output.py`. Examine `validate_extraction()` and `extract_with_retry()`:

1. List the two semantic checks in `validate_extraction()`.
2. Give one example of a validation error where **retry would succeed** (format/structural issue).
3. Give one example where **retry would fail** (information absent from source).
4. What is the `detected_pattern` field used for beyond the immediate extraction run?
5. Why is `tool_choice: {"type": "any"}` used instead of `{"type": "auto"}`?

---

### 4.5 — Explicit Criteria vs Vague Instructions (D4 T4.1)

Compare these two code review prompts:

**Prompt A:**
> "Review this code carefully. Flag any issues you find. Be conservative and only report high-confidence findings."

**Prompt B:**
> "Review this code. Report ONLY:
> 1. Bugs where the code's actual behavior contradicts its documented behavior
> 2. SQL injection, XSS, or authentication bypass vulnerabilities
>
> Skip these categories entirely: code style, naming conventions, unused imports, potential optimizations."

Answer:
1. Which prompt produces more reliable results? Why?
2. What happens to developer trust when a high false-positive category is included alongside accurate categories?
3. Based on Prompt B, what would you do if the security category was generating 80% false positives?

---

### 4.6 — Reflection

Rate your confidence (1–5):

- [ ] I can choose the correct `tool_choice` for any scenario
- [ ] I understand the difference between syntax errors and semantic errors in structured output
- [ ] I know when to make a field nullable vs required
- [ ] I can write a retry-with-error-feedback loop
- [ ] I can write specific categorical review criteria (not vague instructions)
- [ ] I can create effective few-shot examples for consistent classification
