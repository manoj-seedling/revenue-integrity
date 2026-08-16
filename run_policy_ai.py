import csv
from policy_engine import PaperweightPolicy

print("=" * 70)
print("🤖 REVENUE DECISION INTEGRITY - AI-POWERED ENGINE")
print("=" * 70)

# Read opportunities from CSV
opportunities = []
with open("opportunities.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        opportunities.append(row)

print(f"\n📊 Found {len(opportunities)} opportunities")
print("🤖 AI Claim Extraction: ENABLED")
print("📋 Rules Engine: ENABLED")
print("=" * 70)

# Initialize policy engine
policy = PaperweightPolicy()

# Track results
contradicts = []
ai_detected = []
not_verifiable = []
insufficient = []

for opp in opportunities:
    opp_name = opp.get("Name", "Unknown")
    note_text = opp.get("Description", "")
    
    opp_data = {
        "Id": opp.get("Id", ""),
        "Name": opp_name,
        "Amount": float(opp.get("Amount", 0)) if opp.get("Amount") else 0,
        "StageName": opp.get("StageName", ""),
        "CloseDate": opp.get("CloseDate", ""),
        "LastActivityDate": None,
        "CreatedDate": opp.get("CreatedDate", ""),
    }
    
    result = policy.evaluate(
        opp=opp_data,
        tasks=[],
        history=[],
        primary_contact=None,
        note_text=note_text
    )
    
    result["name"] = opp_name
    result["amount"] = opp_data["Amount"]
    
    if result["decision"] == "CONTRADICTS":
        contradicts.append(result)
        if result.get("ai_used", False):
            ai_detected.append(result)
    elif result["decision"] == "NOT_VERIFIABLE":
        not_verifiable.append(result)
    elif result["decision"] == "INSUFFICIENT":
        insufficient.append(result)
    
    # Print each result (summarized to keep output manageable)
    print(f"\n📋 {opp_name[:40]} (${opp_data['Amount']:,.0f})")
    print(f"   Stage: {opp_data['StageName']}")
    print(f"   Decision: {result['decision']}")
    
    if result.get("ai_used", False):
        print(f"   🤖 AI Used: Yes")
        if result.get("extracted_claims"):
            claims = result["extracted_claims"]
            print(f"   📝 Claim Found: {claims.get('claim_found')}")
            print(f"   📝 Champion: {claims.get('champion_engaged')}")
            print(f"   📝 Sentiment: {claims.get('sentiment')}")
            # Show blocker mention if present
            if claims.get('blocker_mentioned'):
                print(f"   📝 Blocker: {claims.get('blocker_mentioned')}")
    else:
        print(f"   🤖 AI Used: No (fallback to rules)")
    
    if result["decision"] == "CONTRADICTS":
        print(f"   🚨 CONTRADICTS!")
        for fact in result["contradicting_facts"][:3]:
            print(f"      ❌ {fact}")
        print(f"   ❓ Question: {result['question']}")
    elif result["decision"] == "NOT_VERIFIABLE":
        print(f"   ⚠️ NOT VERIFIABLE!")
        for fact in result["contradicting_facts"][:3]:
            print(f"      ⚠️ {fact}")
        print(f"   ❓ Question: {result['question']}")
    elif result["decision"] == "INSUFFICIENT":
        print(f"   ℹ️ INSUFFICIENT")
        print(f"   ❓ Question: {result['question']}")

# Summary
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"Total opportunities: {len(opportunities)}")
print(f"🚨 CONTRADICTS: {len(contradicts)}")
if ai_detected:
    print(f"   🤖 AI-detected contradictions: {len(ai_detected)}")
print(f"⚠️ NOT VERIFIABLE: {len(not_verifiable)}")
print(f"ℹ️ INSUFFICIENT: {len(insufficient)}")

if contradicts:
    print("\n🚨 Contradictions found:")
    for c in contradicts[:10]:
        print(f"   - {c['name'][:45]} (${c['amount']:,.0f})")
        if c.get("ai_used", False):
            claims = c.get("extracted_claims", {})
            if claims.get('blocker_mentioned'):
                print(f"      🤖 AI detected blocker claim: {claims.get('blocker_mentioned')}")
            elif claims.get('champion_engaged'):
                print(f"      🤖 AI detected champion engagement: {claims.get('champion_engaged')}")
            else:
                print(f"      🤖 AI detected claim: {c.get('extracted_claims', {}).get('claim_found')}")
    if len(contradicts) > 10:
        print(f"   ... and {len(contradicts) - 10} more")

if not_verifiable:
    print("\n⚠️ NOT VERIFIABLE cases:")
    for n in not_verifiable:
        print(f"   - {n['name'][:45]} (${n['amount']:,.0f})")
        if n.get("extracted_claims", {}).get('blocker_mentioned'):
            print(f"      🤖 AI detected blocker mention with no evidence to verify")

print("\n" + "=" * 70)
print("📋 NEXT STEPS")
print("=" * 70)
print("1. Validate contradictions with managers")
print("2. Track validation rate (precision)")
print("3. Refine AI prompts based on false positives")
print("4. Schedule weekly runs")
print("5. Build reviewer dashboard")