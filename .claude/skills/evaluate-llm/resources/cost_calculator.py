"""
LLM Cost Calculator — 2026-04 定价快照

用法：
    python cost_calculator.py

或在 Python 中：
    from cost_calculator import estimate_monthly_cost, compare_models

    compare_models(
        models=["gemini-3.1-pro", "claude-opus-4.6", "gpt-5.4", "deepseek-v3.2"],
        avg_input_tokens=2000,
        avg_output_tokens=500,
        calls_per_day=10000,
    )

定价数据来源：各厂商 2026-04 公开价目表（请使用前自行核对）。
价格单位：USD per 1M tokens。
"""

# 2026-04 snapshot pricing (USD per 1M tokens)
# NOTE: Update before use — LLM pricing changes frequently.
PRICING = {
    "gemini-3.1-pro":      {"input": 1.25, "output": 5.00,  "cache_discount": 0.25},
    "gemini-3.1-flash":    {"input": 0.15, "output": 0.60,  "cache_discount": 0.25},
    "claude-opus-4.6":     {"input": 15.00,"output": 75.00, "cache_discount": 0.10},
    "claude-sonnet-4.6":   {"input": 3.00, "output": 15.00, "cache_discount": 0.10},
    "gpt-5.4":             {"input": 5.00, "output": 20.00, "cache_discount": 0.50},
    "gpt-5.4-mini":        {"input": 0.50, "output": 2.00,  "cache_discount": 0.50},
    "deepseek-v3.2":       {"input": 0.14, "output": 0.28,  "cache_discount": 0.10},
    "qwen-3.5-max":        {"input": 1.60, "output": 6.40,  "cache_discount": 0.20},
    "glm-5":               {"input": 0.50, "output": 2.00,  "cache_discount": 0.20},
    "kimi-k2.5":           {"input": 1.00, "output": 4.00,  "cache_discount": 0.20},
}


def estimate_monthly_cost(
    model: str,
    avg_input_tokens: int,
    avg_output_tokens: int,
    calls_per_day: int,
    cache_hit_rate: float = 0.0,
    days_per_month: int = 30,
) -> dict:
    """Estimate monthly cost for a single model."""
    if model not in PRICING:
        raise ValueError(f"Unknown model: {model}. Known: {list(PRICING.keys())}")

    p = PRICING[model]
    cached_input = avg_input_tokens * cache_hit_rate
    fresh_input = avg_input_tokens - cached_input

    cost_per_call = (
        (fresh_input / 1_000_000) * p["input"]
        + (cached_input / 1_000_000) * p["input"] * p["cache_discount"]
        + (avg_output_tokens / 1_000_000) * p["output"]
    )

    monthly = cost_per_call * calls_per_day * days_per_month

    return {
        "model": model,
        "cost_per_call_usd": round(cost_per_call, 6),
        "monthly_cost_usd": round(monthly, 2),
        "annual_cost_usd": round(monthly * 12, 2),
    }


def compare_models(
    models: list,
    avg_input_tokens: int,
    avg_output_tokens: int,
    calls_per_day: int,
    cache_hit_rate: float = 0.0,
) -> None:
    """Print a side-by-side cost comparison."""
    print(f"\n{'Model':<22} {'Per Call':>12} {'Monthly':>14} {'Annual':>14}")
    print("-" * 66)
    results = []
    for m in models:
        r = estimate_monthly_cost(
            m, avg_input_tokens, avg_output_tokens, calls_per_day, cache_hit_rate
        )
        results.append(r)
        print(
            f"{r['model']:<22} "
            f"${r['cost_per_call_usd']:>11.6f} "
            f"${r['monthly_cost_usd']:>13,.2f} "
            f"${r['annual_cost_usd']:>13,.2f}"
        )
    print()
    cheapest = min(results, key=lambda x: x["monthly_cost_usd"])
    most = max(results, key=lambda x: x["monthly_cost_usd"])
    ratio = most["monthly_cost_usd"] / cheapest["monthly_cost_usd"] if cheapest["monthly_cost_usd"] else 0
    print(f"Cheapest: {cheapest['model']}  |  Most expensive: {most['model']}  ({ratio:.1f}× gap)")


if __name__ == "__main__":
    print("=== Example: Customer support chatbot, 2K in / 500 out / 10K calls per day ===")
    compare_models(
        models=["gemini-3.1-flash", "gpt-5.4-mini", "deepseek-v3.2", "claude-sonnet-4.6", "qwen-3.5-max"],
        avg_input_tokens=2000,
        avg_output_tokens=500,
        calls_per_day=10000,
        cache_hit_rate=0.4,
    )
