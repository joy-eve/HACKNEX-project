import re


def extract_answer(answer_text):
    match = re.search(
        r"ANSWER:\s*(?:answerable\s*=\s*)?([^\n]+)",
        answer_text,
        re.IGNORECASE
    )

    if not match:
        return None

    value = match.group(1).strip()

    if value.lower() in ["true", "false"]:
        return value.lower() == "true"

    try:
        return float(value)
    except ValueError:
        return value


def extract_result(proof_output):
    matches = re.findall(
        r"RESULT:\s*([-+]?\d+(?:\.\d+)?)",
        proof_output,
        re.IGNORECASE
    )

    if not matches:
        return None

    return float(matches[-1])


def verify_proof_code(proof_code):

    if not proof_code:
        return {
            "valid": False,
            "reason": "No proof code was provided."
        }

    if "import pandas" not in proof_code:
        return {
            "valid": False,
            "reason": "Proof code does not import pandas."
        }

    if (
        "pd.read_csv('data/orders.csv')" not in proof_code
        and 'pd.read_csv("data/orders.csv")' not in proof_code
    ):
        return {
            "valid": False,
            "reason": "Proof code does not read data/orders.csv."
        }

    if "StringIO" in proof_code:
        return {
            "valid": False,
            "reason": "Proof code appears to recreate the dataset instead of reading the CSV."
        }

    if not re.search(r"\bresult\s*=", proof_code):
        return {
            "valid": False,
            "reason": "Proof code does not calculate a result variable."
        }

    if "RESULT:" not in proof_code:
        return {
            "valid": False,
            "reason": "Proof code does not print a RESULT."
        }

    # Reject hardcoded result assignments such as:
    # result = 9
    # result = 9.0
    # result = -5
    hardcoded_result = re.search(
        r"\bresult\s*=\s*[-+]?\d+(?:\.\d+)?\s*(?:#.*)?$",
        proof_code,
        re.IGNORECASE | re.MULTILINE
    )

    if hardcoded_result:
        return {
            "valid": False,
            "reason": "Proof code hardcodes the final result instead of calculating it."
        }

    return {
        "valid": True,
        "reason": "Proof code passed structural checks."
    }


def verify(answer_text, proof_output, proof_code=None):

    claimed = extract_answer(answer_text)

    if claimed is None:
        return {
            "verified": False,
            "reason": "Could not extract the agent's answer."
        }

    # Handle refusal
    if isinstance(claimed, bool):

        if claimed is False:
            return {
                "verified": True,
                "refused": True,
                "reason": "Agent correctly refused to provide an unreliable answer."
            }

        return {
            "verified": False,
            "reason": "Agent returned answerable=true instead of a numerical answer."
        }

    if proof_code is not None:

        proof_check = verify_proof_code(proof_code)

        if not proof_check["valid"]:
            return {
                "verified": False,
                "reason": proof_check["reason"]
            }

    calculated = extract_result(proof_output)

    if calculated is None:
        return {
            "verified": False,
            "reason": "Executed proof code did not produce a RESULT."
        }

    if claimed == calculated:
        return {
            "verified": True,
            "refused": False,
            "reason": "Agent answer matches the executed proof code.",
            "answer": calculated
        }

    return {
        "verified": False,
        "reason": f"Agent claimed {claimed}, but proof code calculated {calculated}.",
        "claimed": claimed,
        "calculated": calculated
    }