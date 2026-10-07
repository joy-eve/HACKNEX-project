import os
import pandas as pd
from dotenv import load_dotenv
from google import genai

from src.cleaner import inspect_all_datasets

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

with open("policy.txt", "r", encoding="utf-8") as f:
    policy = f.read()

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")


def ask_agent(question):

    data_quality = inspect_all_datasets()

    prompt = (
        "You are a Proof-Carrying Data Analyst.\n\n"

        "Your job is to answer the user's question using the provided datasets.\n\n"

        "IMPORTANT RULES:\n"
        + policy
        + "\n\n"

        "AVAILABLE DATA:\n\n"

        "CUSTOMERS TABLE:\n"
        "Columns:\n"
        + str(customers.columns.tolist())
        + "\n\n"
        "Data:\n"
        + customers.to_string(index=False)
        + "\n\n"

        "ORDERS TABLE:\n"
        "Columns:\n"
        + str(orders.columns.tolist())
        + "\n\n"
        "Data:\n"
        + orders.to_string(index=False)
        + "\n\n"

        "DATA QUALITY REPORT:\n"
        + str(data_quality)
        + "\n\n"

        "USER QUESTION:\n"
        + question
        + "\n\n"

        "ANALYSIS PROCEDURE:\n"
        "Before giving an answer, follow these steps internally:\n"
        "1. Identify exactly what the question is asking.\n"
        "2. Identify which dataset and columns are required.\n"
        "3. Check the relevant rows carefully.\n"
        "4. Perform the calculation independently.\n"
        "5. Double-check the calculation against the actual dataset.\n"
        "6. Only then provide the final answer.\n"
        "7. The proof code must independently perform the same calculation.\n\n"

        "IMPORTANT ANSWERING RULES:\n"
        "- Base your answer on the actual data.\n"
        "- Use the data quality report when deciding whether the question is answerable.\n"
        "- Do not invent values.\n"
        "- Do not guess.\n"
        "- Check the actual values before answering.\n"
        "- For counting questions, count the matching rows carefully.\n"
        "- Currency differences do not matter for simple counts.\n"
        "- Date differences do not matter when the calculation does not depend on dates.\n"
        "- If monetary values from different currencies must be combined and no exchange rates exist, refuse.\n"
        "- If required data is missing, refuse.\n"
        "- If contradictory information affects the answer, refuse.\n"
        "- If an ambiguous date can change the answer, refuse.\n"
        "- A refusal must use exactly: ANSWER: answerable = false\n"
        "- A refusal must include a clear REASON.\n"
        "- Do not generate numerical proof code for a refused question.\n\n"

        "CRITICAL PROOF CODE RULES:\n"
        "- Only generate proof code if the question is answerable.\n"
        "- The proof code MUST read the original CSV files.\n"
        "- The proof code MUST NOT copy dataset rows.\n"
        "- NEVER use io.StringIO with copied CSV data.\n"
        "- NEVER hardcode the final answer.\n"
        "- The proof must independently calculate the answer.\n"
        "- Use pd.read_csv('data/orders.csv') when orders are needed.\n"
        "- Use pd.read_csv('data/customers.csv') when customers are needed.\n"
        "- Store the calculated answer in a variable named result.\n"
        "- Print the result using: print(f'RESULT: {result}')\n"
        "- The value printed after RESULT must come from the calculation.\n\n"

        "VALID PROOF CODE EXAMPLE:\n"
        "orders_df = pd.read_csv('data/orders.csv')\n"
        "completed_orders = orders_df[orders_df['status'] == 'completed']\n"
        "result = len(completed_orders)\n"
        "print(f'RESULT: {result}')\n\n"

        "RETURN FORMAT FOR ANSWERABLE QUESTIONS:\n"
        "ANSWER:\n"
        "<numerical answer>\n\n"
        "REASON:\n"
        "<reason>\n\n"
        "PROOF CODE:\n"
        "<complete executable Python code in a Python code block>\n\n"

        "RETURN FORMAT FOR UNANSWERABLE QUESTIONS:\n"
        "ANSWER:\n"
        "answerable = false\n\n"
        "REASON:\n"
        "<clear explanation>\n\n"

        "Return only ONE ANSWER section.\n"
        "Do not provide multiple answers."
    )

    chat = client.chats.create(model="gemini-3.5-flash-lite")
    response = chat.send_message(prompt)

    return response.text


if __name__ == "__main__":
    question = input("Ask a data question: ")
    print("\n" + ask_agent(question))