"""
Multi-API calls + LLM orchestration powered by HTTPayer
Demonstrates x402 payment extraction and decoding
"""

import os
import json
import base64
from dotenv import load_dotenv
from httpayer import HTTPayerClient

load_dotenv()

# Initialize client
EVM_PRIVATE_KEY = os.getenv("EVM_PRIVATE_KEY")

if not EVM_PRIVATE_KEY:
    raise ValueError("EVM_PRIVATE_KEY environment variable is not set.")

client = HTTPayerClient(
    private_key=EVM_PRIVATE_KEY,
    network="base"  # Network to pay on
)

print()
print("=== HTTPayer Multi-API Orchestration ===")
print("Gloria AI + Nansen + Heurist + LLM Chat")
print()


def decode_payment_response(header_value: str) -> dict:
    """Decode x-payment-response header (base64 encoded JSON)"""
    try:
        decoded = base64.b64decode(header_value).decode('utf-8')
        return json.loads(decoded)
    except Exception as e:
        print(f"Warning: Could not decode payment response: {e}")
        return {"raw": header_value}


def extract_payment_info(response):
    """Extract and decode payment headers from response"""
    payment_info = {}

    # Extract x-client-payment (client's tx to HTTPayer)
    if "x-client-payment" in response.headers:
        payment_info["client_payment"] = response.headers["x-client-payment"]
        print(f"[Payment] Client TX: {payment_info['client_payment']}")

    # Extract x-payment-response (HTTPayer's tx to target API)
    payment_response_header = (
        response.headers.get("payment-response") or
        response.headers.get("x-payment-response")
    )

    if payment_response_header:
        decoded = decode_payment_response(payment_response_header)
        payment_info["payment_response"] = decoded
        print(f"[Payment] HTTPayer TX: {json.dumps(decoded, indent=2)}")

    return payment_info

# === Step 1: Get Gloria AI news ===
def get_gloria_news():
    """Fetch AI and crypto news from Gloria AI"""
    print("[Step 1] Fetching Gloria AI news...")

    GLORIA_AI_URL = "https://api.itsgloria.ai/news?feed_categories=ai,crypto"

    response = client.request(
        method="GET",
        url=GLORIA_AI_URL,
        headers={"Accept": "application/json"}
    )

    response.raise_for_status()

    # Extract payment info
    print()
    payment_info = extract_payment_info(response)
    print()

    data = response.json()
    print(f"[Gloria] Received {len(data)} news items")

    # Parse news summaries
    gloria_news_summaries = {}
    for item in data:
        signal = item.get("signal")
        sentiment = item.get("sentiment")
        summary = item.get("short_context") or "No summary available."
        source = item.get("sources")[0] if item.get("sources") else "Unknown"

        gloria_news_summaries[signal] = {
            "sentiment": sentiment,
            "summary": summary,
            "source": source,
        }

    return gloria_news_summaries, payment_info

# === Step 2: Get Nansen smart money data ===
def get_nansen_data():
    """Fetch smart money netflow data from Nansen"""
    print("[Step 2] Fetching Nansen smart money data...")

    NANSEN_API_URL = "https://nansen.api.corbits.dev/api/v1/smart-money/netflow"

    request_data = {
        "chains": ["ethereum", "solana"],
        "filters": {
            "exclude_smart_money_labels": ["30D Smart Trader"],
            "include_native_tokens": False,
            "include_smart_money_labels": ["Fund", "Smart Trader"],
            "include_stablecoins": True
        },
        "pagination": {
            "page": 1,
            "per_page": 10
        },
        "order_by": [
            {
                "field": "net_flow_30d_usd",
                "direction": "DESC"
            }
        ]
    }

    response = client.request(
        method="POST",
        url=NANSEN_API_URL,
        headers={"Content-Type": "application/json"},
        json=request_data
    )

    response.raise_for_status()

    # Extract payment info
    print()
    payment_info = extract_payment_info(response)
    print()

    nansen_data = response.json()

    # Extract tokens and sectors
    token_symbols = [item['token_symbol'] for item in nansen_data.get("data", [])]
    sectors = set()
    filtered_nansen_data = {}

    print(f"[Nansen] Received {len(nansen_data.get('data', []))} smart money flows:")
    for item in nansen_data.get("data", []):
        print(f"  • {item['token_symbol']}: ${item['net_flow_30d_usd']:,.2f} | {', '.join(item['token_sectors'])}")
        for sector in item['token_sectors']:
            sectors.add(sector)

        filtered_nansen_data[item['token_symbol']] = {
            "net_flow_30d_usd": item['net_flow_30d_usd'],
            "token_sectors": item['token_sectors']
        }

    return filtered_nansen_data, token_symbols, sectors, payment_info

# === Step 3: Get Heurist news search ===
def get_heurist_search(token_symbols, sectors):
    """Search for crypto news using Heurist AI based on Nansen tokens"""
    print("[Step 3] Searching crypto news with Heurist AI...")

    HEURIST_API_URL = "https://mesh.heurist.xyz/x402/agents/ExaSearchDigestAgent/exa_web_search"

    search_term = f"Recent cryptocurrency news and market analysis for tokens: {', '.join(token_symbols)}. Focus on {', '.join(sectors)} sectors."
    print(f"[Heurist] Search term: {search_term[:100]}...")

    data = {
        "search_term": search_term,
        "limit": 5,
        "time_filter": "past_month"
    }

    response = client.request(
        method="POST",
        url=HEURIST_API_URL,
        headers={"Content-Type": "application/json"},
        json=data
    )

    response.raise_for_status()

    # Extract payment info
    print()
    payment_info = extract_payment_info(response)
    print()

    heurist_data = response.json().get("result", {}).get("data", {})
    print(f"[Heurist] Search results received")

    return heurist_data, payment_info

# === Step 4: Summarize with LLM ===
def summarize_with_llm(gloria_data, nansen_data, heurist_data, temperature=0.7):
    """Generate investment insights using LLM based on all gathered data"""
    print("[Step 4] Generating investment analysis with LLM...")

    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant that analyzes cryptocurrency smart money flows and related news to provide actionable insights."
        },
        {
            "role": "user",
            "content": f"""Analyze the following data:

GLORIA AI NEWS:
{json.dumps(gloria_data, indent=2)}

SMART MONEY TOKEN FLOWS (from Nansen):
{json.dumps(nansen_data, indent=2)}

RELATED NEWS & MARKET ANALYSIS (from Heurist):
{json.dumps(heurist_data, indent=2)}

Provide a concise summary that:
1. Identifies which tokens smart money is accumulating or selling
2. Explains potential reasons based on the news articles
3. Highlights key trends or opportunities
4. Suggests how an investor should position their portfolio based on these insights"""
        }
    ]

    url = "https://api.httpayer.com/llm/chat"

    payload = {
        "messages": messages,
        "temperature": temperature
    }
    headers = {"Content-Type": "application/json"}

    direct_client = HTTPayerClient(
        private_key=EVM_PRIVATE_KEY,
        network="base", # Network to pay on
        privacy_mode=False # Direct x402 payment
    )

    response = direct_client.request(
        method="POST",
        url=url,
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    # Extract payment info
    print()
    payment_info = extract_payment_info(response)
    print()

    llm_data = response.json()
    print("[LLM] Investment analysis generated")

    return llm_data, payment_info


# === Main execution ===
def main():
    """Run the multi-API orchestration demo"""
    try:
        # Step 1: Get Gloria AI news
        gloria_summaries, gloria_payment = get_gloria_news()
        print()

        # Step 2: Get Nansen smart money data
        nansen_data, token_symbols, sectors, nansen_payment = get_nansen_data()
        print()

        # Step 3: Search Heurist for related news
        heurist_data, heurist_payment = get_heurist_search(token_symbols, list(sectors))
        print()

        # Step 4: Generate LLM summary
        llm_response, llm_payment = summarize_with_llm(
            gloria_summaries,
            nansen_data,
            heurist_data,
            temperature=0.7
        )
        print()

        # Display final results
        print("=" * 60)
        print("=== Analysis Complete ===")
        print("=" * 60)
        print()
        print("LLM Investment Analysis:")
        print(llm_response.get("response", ""))
        print()

        # Summary of payments made
        print("=" * 60)
        print("=== Payment Summary ===")
        print("=" * 60)
        print(f"Total API calls made: 4")
        print(f"  1. Gloria AI news")
        print(f"  2. Nansen smart money netflow")
        print(f"  3. Heurist AI search")
        print(f"  4. LLM chat analysis")
        print()

    except Exception as e:
        print(f"Error during execution: {e}")
        raise


if __name__ == "__main__":
    main()