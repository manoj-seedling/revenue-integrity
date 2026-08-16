import csv
from policy_engine import PaperweightPolicy

# Read opportunities from CSV
opportunities = []

with open("opportunities.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        opportunities.append(row)

print(f"📊 Found {len(opportunities)} opportunities in CSV")
print("=" * 70)

# Initialize policy engine
policy = PaperweightPolicy()

# Track results
contradicts = []
supports = []
insufficient = []

for opp in opportunities:
    opp_name = opp.get("Name", "Unknown")
    opp_id = opp.get("Id", "")
    
    # Build data structure for policy engine
    opp_data = {
        "Id": opp_id,
        "Name": opp_name,
        "Amount": float(opp.get("Amount", 0)) if opp.get("Amount") else 0,
        "StageName": opp.get("StageName", ""),
        "CloseDate": opp.get("CloseDate", ""),
        "LastActivityDate": None,
        "CreatedDate": opp.get("CreatedDate", ""),
    }
    
    # Use Description as the "note" text
    note_text = opp.get("Description", "")
    
    # Run policy with empty tasks and history
    result = policy.evaluate(
        opp=opp_data,
        tasks=[],
        history=[],
        primary_contact=None,
        note_text=note_text
    )
    
    # Store result
    result["name"] = opp_name
    result["amount"] = opp_data["Amount"]
    result["stage"] = opp_data["StageName"]
    
    if result["decision"] == "CONTRADICTS":
        contradicts.append(result)
    elif result["decision"] == "SUPPORTS":
        supports.append(result)
    else:
        insufficient.append(result)
    
    # Print each result
    print(f"\n📋 {opp_name[:50]} (${opp_data['Amount']:,.0f})")
    print(f"   Stage: {opp_data['StageName']}")
    print(f"   Decision: {result['decision']}")
    print(f"   Confidence: {result['confidence']:.0%}")
    
    if result["decision"] == "CONTRADICTS":
        print(f"   🚨 CONTRADICTS!")
        for fact in result["contradicting_facts"]:
            print(f"      ❌ {fact}")
        print(f"   ❓ Question: {result['question']}")
    elif result["decision"] == "SUPPORTS":
        print(f"   ✅ SUPPORTS")
        for fact in result["supporting_facts"]:
            print(f"      ✅ {fact}")
    else:
        print(f"   ℹ️ INSUFFICIENT")
        print(f"   ❓ Question: {result['question']}")

# Summary
print("\n" + "=" * 70)
print("📊 SUMMARY")
print("=" * 70)
print(f"Total opportunities: {len(opportunities)}")
print(f"🚨 CONTRADICTS: {len(contradicts)}")
print(f"✅ SUPPORTS: {len(supports)}")
print(f"ℹ️ INSUFFICIENT: {len(insufficient)}")

if contradicts:
    print("\n🚨 Contradicts found:")
    for c in contradicts:
        print(f"   - {c['name'][:50]} (${c['amount']:,.0f})")

if insufficient and not contradicts:
    print("\n💡 No contradictions found.")
    print("   This is because the CSV doesn't have:")
    print("   - Tasks linked to buyer")
    print("   - Opportunity history (stage/date changes)")
    print("   - LastActivityDate")
    print("   - Notes with 'engaged' or 'champion' keywords")
    print("\n   To find real contradictions, we need more data:")
    print("   - Export Tasks from Workbench")
    print("   - Export OpportunityHistory from Workbench")