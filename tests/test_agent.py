from src.verifier import verify


def test_correct_answer():
    answer = "ANSWER:\n9"
    proof_output = "RESULT: 9"

    proof_code = """
import pandas as pd

orders_df = pd.read_csv('data/orders.csv')
completed_orders = orders_df[orders_df['status'] == 'completed']
result = len(completed_orders)
print(f'RESULT: {result}')
"""

    result = verify(answer, proof_output, proof_code)

    assert result["verified"] is True


def test_wrong_answer_is_rejected():
    answer = "ANSWER:\n8"
    proof_output = "RESULT: 9"

    proof_code = """
import pandas as pd

orders_df = pd.read_csv('data/orders.csv')
completed_orders = orders_df[orders_df['status'] == 'completed']
result = len(completed_orders)
print(f'RESULT: {result}')
"""

    result = verify(answer, proof_output, proof_code)

    assert result["verified"] is False


def test_refusal_is_verified():
    answer = "ANSWER:\nanswerable = false"

    result = verify(answer, "", None)

    assert result["verified"] is True
    assert result["refused"] is True


def test_missing_result_is_rejected():
    answer = "ANSWER:\n9"
    proof_output = "Number of completed orders: 9"

    proof_code = """
import pandas as pd

orders_df = pd.read_csv('data/orders.csv')
completed_orders = orders_df[orders_df['status'] == 'completed']
result = len(completed_orders)
print("Number of completed orders:", result)
"""

    result = verify(answer, proof_output, proof_code)

    assert result["verified"] is False


def test_hardcoded_result_is_rejected():
    answer = "ANSWER:\n9"
    proof_output = "RESULT: 9"

    proof_code = """
import pandas as pd

orders_df = pd.read_csv('data/orders.csv')
result = 9
print(f'RESULT: {result}')
"""

    result = verify(answer, proof_output, proof_code)

    assert result["verified"] is False