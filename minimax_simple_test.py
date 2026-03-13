#!/usr/bin/env python3
"""
Simple MiniMax API test
"""

from openai import OpenAI

# Initialize MiniMax client
client = OpenAI(
    base_url="https://api.minimax.io/v1",
    api_key="your-api-key-here"  # Replace with your key
)

# Test simple completion
response = client.chat.completions.create(
    model="MiniMax-M2.5",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to calculate Bollinger Bands for a price series."}
    ],
    temperature=0.7,
    max_tokens=1000
)

print(response.choices[0].message.content)
print(f"\nTokens used: {response.usage.total_tokens}")
