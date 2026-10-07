import re

from src.agent import ask_agent
from src.executor import execute_code
from src.verifier import verify


def extract_proof_code(agent_response):

    match = re.search(
        r"PROOF CODE:.*?```python\s*(.*?)```",
        agent_response,
        re.IGNORECASE | re.DOTALL
    )

    if not match:
        return None

    return match.group(1).strip()


def main():

    question = input("Ask a data question: ")

    print("\nGenerating analysis...\n")

    agent_response = ask_agent(question)

    print("===== AGENT RESPONSE =====")
    print(agent_response)

    # Check whether the agent refused
    if "answerable = false" in agent_response.lower():

        print("\n===== VERIFICATION =====")

        verification = verify(
            agent_response,
            "",
            None
        )

        if verification["verified"]:
            print("✅ VERIFIED REFUSAL")
            print(verification["reason"])
        else:
            print("❌ REJECTED")
            print(verification["reason"])

        return

    # Extract proof code
    proof_code = extract_proof_code(agent_response)

    if not proof_code:
        print("\n❌ Could not extract proof code.")
        return

    print("\n===== EXECUTING PROOF =====")

    execution = execute_code(proof_code)

    if not execution["success"]:
        print("❌ Proof code failed.")
        print(execution["error"])
        return

    print(execution["output"])

    print("===== VERIFICATION =====")

    verification = verify(
        agent_response,
        execution["output"],
        proof_code
    )

    if verification["verified"]:

        if verification.get("refused"):
            print("✅ VERIFIED REFUSAL")
            print(verification["reason"])

        else:
            print("✅ VERIFIED")
            print("Final answer:", verification["answer"])

    else:
        print("❌ REJECTED")
        print(verification["reason"])


if __name__ == "__main__":
    main()