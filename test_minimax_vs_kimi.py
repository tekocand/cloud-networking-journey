#!/usr/bin/env python3
"""
MiniMax vs Kimi comparison test
Tests coding, reasoning, and speed
"""

import os
import time
from openai import OpenAI

# Configuration
MINIMAX_BASE_URL = "https://api.minimax.io/v1"
KIMI_BASE_URL = "https://api.moonshot.cn/v1"

# Get API keys from environment or replace directly
MINIMAX_API_KEY = os.getenv("MINIMAX_API_KEY", "your-minimax-key")
KIMI_API_KEY = os.getenv("KIMI_API_KEY", "your-kimi-key")

# Test prompts
TESTS = {
    "coding": """Write a Python function to calculate the Relative Strength Index (RSI) 
for a given list of price data. Include proper error handling and docstring.""",
    
    "reasoning": """A trader has $10,000. They make 3 trades:
1. +20% gain
2. -15% loss  
3. +10% gain

What's their final balance? Show your calculation step by step.""",
    
    "tool_use": """You have access to these functions:
- get_stock_price(symbol: str)
- calculate_position_size(account_balance: float, risk_percent: float, stop_loss_pips: float)

A user says: "I want to risk 2% on EURUSD with a 50 pip stop, my account is $5000"

What function calls would you make?""",
}

def test_model(client, model_name, test_name, prompt):
    """Run a single test and return results"""
    start_time = time.time()
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        elapsed = time.time() - start_time
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens if response.usage else 0
        
        return {
            "success": True,
            "content": content,
            "time": elapsed,
            "tokens": tokens_used,
            "speed": tokens_used / elapsed if elapsed > 0 else 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "time": time.time() - start_time
        }

def run_comparison():
    """Run all tests comparing MiniMax and Kimi"""
    
    # Initialize clients
    minimax = OpenAI(
        base_url=MINIMAX_BASE_URL,
        api_key=MINIMAX_API_KEY
    )
    
    kimi = OpenAI(
        base_url=KIMI_BASE_URL,
        api_key=KIMI_API_KEY
    )
    
    results = {
        "MiniMax-M2.5": {},
        "kimi-k2.5": {}
    }
    
    print("=" * 60)
    print("MiniMax vs Kimi Comparison Test")
    print("=" * 60)
    
    for test_name, prompt in TESTS.items():
        print(f"\n{'='*60}")
        print(f"Test: {test_name.upper()}")
        print(f"{'='*60}")
        
        # Test MiniMax
        print("\n🚀 MiniMax M2.5...")
        mm_result = test_model(minimax, "MiniMax-M2.5", test_name, prompt)
        results["MiniMax-M2.5"][test_name] = mm_result
        
        if mm_result["success"]:
            print(f"✅ Time: {mm_result['time']:.2f}s | Tokens: {mm_result['tokens']} | Speed: {mm_result['speed']:.1f} tok/s")
            print(f"Preview: {mm_result['content'][:200]}...")
        else:
            print(f"❌ Error: {mm_result['error']}")
        
        # Test Kimi
        print("\n🌙 Kimi K2.5...")
        kimi_result = test_model(kimi, "kimi-k2.5", test_name, prompt)
        results["kimi-k2.5"][test_name] = kimi_result
        
        if kimi_result["success"]:
            print(f"✅ Time: {kimi_result['time']:.2f}s | Tokens: {kimi_result['tokens']} | Speed: {kimi_result['speed']:.1f} tok/s")
            print(f"Preview: {kimi_result['content'][:200]}...")
        else:
            print(f"❌ Error: {kimi_result['error']}")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    for model in ["MiniMax-M2.5", "kimi-k2.5"]:
        print(f"\n{model}:")
        total_time = sum(r["time"] for r in results[model].values() if r.get("success"))
        total_tokens = sum(r.get("tokens", 0) for r in results[model].values() if r.get("success"))
        print(f"  Total time: {total_time:.2f}s")
        print(f"  Total tokens: {total_tokens}")
        print(f"  Avg speed: {total_tokens/total_time:.1f} tok/s" if total_time > 0 else "  N/A")
    
    return results

if __name__ == "__main__":
    # Check for API keys
    if MINIMAX_API_KEY == "your-minimax-key":
        print("⚠️  Set MINIMAX_API_KEY environment variable or edit the script")
    if KIMI_API_KEY == "your-kimi-key":
        print("⚠️  Set KIMI_API_KEY environment variable or edit the script")
    
    if MINIMAX_API_KEY != "your-minimax-key" and KIMI_API_KEY != "your-kimi-key":
        run_comparison()
    else:
        print("\nAdd your API keys to run the comparison test.")
