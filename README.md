# Proof-Carrying Data Analyst

An Agentic GenAI data analyst that answers questions about datasets and provides executable proof code for numerical answers.

## How It Works

1. User asks a data question.
2. AI agent analyzes the available data.
3. Agent generates an answer and Python proof code.
4. Proof code is executed on the original dataset.
5. The verifier compares the AI answer with the calculated result.
6. The answer is verified or rejected.
7. If the data is insufficient or unreliable, the agent refuses to answer.

## Architecture

User Question
↓
AI Agent
↓
Generated Python Proof
↓
Proof Executor
↓
Verifier
↓
Verified Answer / Rejection / Refusal

## Features

- AI-powered data analysis
- Executable proof for numerical answers
- Automatic answer verification
- Rejects incorrect answers
- Rejects hardcoded proof results
- Refuses unreliable calculations
- Handles currency-related ambiguity
- Automated verification tests

## Project Structure

HNX26PSI08/
├── data/
├── src/
├── tests/
├── main.py
├── policy.txt
├── requirements.txt
└── README.md

## Requirements

- Python 3.13+
- Gemini API key
- Internet connection

## Setup

Install dependencies:

    pip install -r requirements.txt

Create a `.env` file:

    GEMINI_API_KEY=your_api_key_here

Do not upload the `.env` file to GitHub.

## Run

    python main.py

Example question:

    How many completed orders are there?

The system generates proof code, executes it against the dataset, and verifies the result.

## Testing

Run:

    python -m pytest

The tests verify correct answers, incorrect answers, refusals, missing results, and hardcoded proof results.

## Core Principle

The system does not blindly trust the AI's answer.

Every numerical answer must be backed by executable Python code that reads the actual dataset and independently calculates the result.

If the calculated result does not match the AI's answer, the answer is rejected.

## Hackathon

Challenge: HNX26PSI08  
Theme: Proof-Carrying Data Analyst (Agentic GenAI)

Built for HackNex Hackathon 2026.
