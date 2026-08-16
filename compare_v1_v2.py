"""
Compare v1 (original) and v2 (refined) classification results.
Run this after both run_policy_ai.py (v1) and run_policy_v2.py have been executed.
"""

import csv

print("=" * 70)
print("📊 V1 vs V2 COMPARISON")
print("=" * 70)

# Load v1 results (from run_policy_ai.py output)
# Note: v1 output is in the terminal, not saved to a file.
# We'll manually input the known v1 results from the earlier run.

print("\n🔍 V1 (Original) Results:")
print("-" * 50)
print("Total opportunities: 120")
print("CONTRADICTS: 12")
print("NOT_VERIFIABLE: 0")
print("INSUFFICIENT: 108")

print("\n🔍 V2 (Refined) Results:")
print("-" * 50)

# Try to read v2 results from file
try:
    with open("v2_results_summary.txt", "r", encoding="utf-8") as f:
        content = f.read()
        print(content)
except FileNotFoundError:
    print("⚠️ v2_results_summary.txt not found.")
    print("   Please run run_policy_v2.py first to generate v2 results.")
    print("\n" + "=" * 70)
    print("📋 COMPARISON FRAMEWORK")
    print("=" * 70)
    print("""
V1 (Original):
- Claim extraction: Single claim per note (LLM + keyword fallback)
- Evidence: Limited evidence checks (tasks, activity, history)
- Classification: CONTRADICTS, UNSUPPORTED, INSUFFICIENT

V2 (Refined):
- Claim extraction: Multiple granular claims per note
- Evidence: Registry-aware (NOT_VERIFIABLE when sources missing)
- Classification: SUPPORTED, UNSUPPORTED, CONTRADICTED, NOT_VERIFIABLE, INSUFFICIENT

Key difference: V2 separates:
- UNSUPPORTED (evidence exists but empty)
- NOT_VERIFIABLE (evidence source missing entirely)
""")
    exit(0)

# Parse v2 results
v2_stats = {}
for line in content.split('\n'):
    if ':' in line:
        parts = line.split(':')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip().split('(')[0].strip()
            if key in ["CONTRADICTS", "SUPPORTED", "UNSUPPORTED", "NOT_VERIFIABLE", "INSUFFICIENT"]:
                try:
                    v2_stats[key] = int(value)
                except:
                    pass

print("\n" + "=" * 70)
print("📊 COMPARISON MATRIX")
print("=" * 70)
print(f"{'Metric':<20} {'V1':<10} {'V2':<10} {'Change':<10}")
print("-" * 50)

v1_stats = {
    "CONTRADICTS": 12,
    "NOT_VERIFIABLE": 0,
    "INSUFFICIENT": 108,
    "SUPPORTED": 0
}

metrics = ["CONTRADICTS", "NOT_VERIFIABLE", "SUPPORTED", "INSUFFICIENT"]
for metric in metrics:
    v1_val = v1_stats.get(metric, 0)
    v2_val = v2_stats.get(metric, 0)
    change = v2_val - v1_val
    change_str = f"+{change}" if change > 0 else str(change) if change < 0 else "0"
    print(f"{metric:<20} {v1_val:<10} {v2_val:<10} {change_str:<10}")

print("\n" + "=" * 70)
print("🔍 INTERPRETATION")
print("=" * 70)

if v2_stats.get("NOT_VERIFIABLE", 0) > 0:
    print(f"✅ V2 correctly classifies {v2_stats['NOT_VERIFIABLE']} claims as NOT_VERIFIABLE")
    print("   These would have been misclassified as UNSUPPORTED in V1.")
    print("   This is a positive change: the system now knows what it cannot test.")

if v2_stats.get("SUPPORTED", 0) > 0:
    print(f"✅ V2 found {v2_stats['SUPPORTED']} claims with supporting evidence.")

if v2_stats.get("CONTRADICTS", 0) < v1_stats.get("CONTRADICTS", 0):
    diff = v1_stats.get("CONTRADICTS", 0) - v2_stats.get("CONTRADICTS", 0)
    print(f"✅ V2 reduced CONTRADICTS by {diff}, reclassifying them as NOT_VERIFIABLE.")

print("\n" + "=" * 70)
print("📋 KEY INSIGHTS")
print("=" * 70)

# Load claims from claims.csv for additional context
try:
    with open("claims.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        claim_count = sum(1 for _ in reader)
    print(f"\n📊 Claims tracked in validation: {claim_count} claims across 12 opportunities")
except FileNotFoundError:
    print("\nℹ️ claims.csv not found - skipping validation context")

print("\n" + "=" * 70)
print("📋 NEXT STEPS")
print("=" * 70)
print("1. If NOT_VERIFIABLE count is high (60%+), this is expected given limited CSV data")
print("2. To reduce NOT_VERIFIABLE, add more evidence sources (tasks, contacts, history)")
print("3. To improve UNSUPPORTED→SUPPORTED, ensure reps log activities and next steps")
print("4. Prepare for genuine human review with revised policy")