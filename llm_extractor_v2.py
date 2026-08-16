import os
import json
from dotenv import load_dotenv
from groq import Groq
from evidence_registry import CLAIM_TAXONOMY_V2

# Load environment variables from .env file
load_dotenv()

# Retrieve API key from environment
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable not set. Please set it in a .env file.")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Use a supported model (check Groq docs for latest)

MODEL_NAME = "llama-3.3-70b-versatile"


def extract_claims_v2(note_text):
    """
    Extract multiple granular claims from a sales rep note.
    Returns a list of claim objects.
    """
    if not note_text or len(note_text.strip()) < 5:
        return []

    prompt = f"""
You are a structured data extractor for sales notes.

Claim Taxonomy:
{CLAIM_TAXONOMY_V2}

Extract ALL claims from the note below. Each claim should be a separate object.

Return ONLY JSON with this exact structure:
{{
    "claims": [
        {{
            "source_text": "Exact text from the note that supports this claim",
            "normalized_claim": "Clear, neutral description of the claim",
            "claim_type": "champion_engaged|deal_momentum|decision_maker_support|budget_approved|blocker_absence|legal_process_active|close_timeline|sentiment",
            "polarity": "positive|negative|neutral|unknown",
            "subject": "champion|decision_maker|budget|legal|process|timeline|sentiment|unknown",
            "timeframe": "Specific timeframe mentioned, or null"
        }}
    ]
}}

Note: "{note_text}"

Return ONLY JSON, no other text.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You extract structured claims from sales notes."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0,
            max_tokens=500,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        claims = result.get("claims", [])

        # Add raw note for context
        for claim in claims:
            claim["raw_note"] = note_text[:300]

        return claims

    except Exception as e:
        print(f"❌ LLM Extraction Error: {e}")
        return []


# Deduplicate claims based on normalized fields
def deduplicate_claims(claims):
    seen = set()
    unique = []
    for claim in claims:
        key = (
            claim.get("claim_type", ""),
            claim.get("subject", ""),
            claim.get("polarity", ""),
            claim.get("timeframe", "")
        )
        if key not in seen:
            seen.add(key)
            unique.append(claim)
    return unique


# Test function
if __name__ == "__main__":
    test_notes = [
        "Champion is engaged. Legal review next week. Should close by end of quarter.",
        "Deal is warm. Sarah is fully bought in. Working on pricing. Budget approved.",
        "Everything is green. CFO is supportive. No blockers.",
        "No update. Still waiting.",
        "Strong momentum. Champion committed. Legal review in progress."
    ]

    print("🧪 Testing Granular Claim Extraction")
    print("=" * 70)
    for note in test_notes:
        claims = extract_claims_v2(note)
        print(f"\n📝 Note: {note[:60]}...")
        print(f"   Claims found (raw): {len(claims)}")
        claims = deduplicate_claims(claims)
        print(f"   Claims found (deduplicated): {len(claims)}")
        for claim in claims:
            print(f"   - {claim.get('claim_type')}: {claim.get('normalized_claim')}")
            if claim.get('timeframe'):
                print(f"     Timeframe: {claim.get('timeframe')}")
        print("   " + "-" * 40)

    print("\n" + "=" * 70)
    print("✅ Test complete.")