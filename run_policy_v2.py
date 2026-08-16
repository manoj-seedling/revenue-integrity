import csv
import json
from evidence_registry import get_available_summary
from llm_extractor_v2 import extract_claims_v2
from policy_engine_v2 import evaluate_note


def load_opportunities(filename="opportunities.csv"):
    """Load opportunities from CSV."""
    opportunities = []
    with open(filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            opp = {
                "Id": row.get("Id", ""),
                "Name": row.get("Name", "Unknown"),
                "Amount": float(row.get("Amount", 0)) if row.get("Amount") else 0,
                "StageName": row.get("StageName", ""),
                "CloseDate": row.get("CloseDate", ""),
                "NextStep": row.get("NextStep", ""),
                "Type": row.get("Type", ""),
                "LeadSource": row.get("LeadSource", ""),
                "Description": row.get("Description", "")
            }
            opportunities.append(opp)
    return opportunities


def main():
    print("=" * 70)
    print("🤖 REVENUE DECISION INTEGRITY - V2")
    print("   Granular Extraction + Evidence Registry")
    print("=" * 70)

    # Show evidence availability
    summary = get_available_summary()
    print(f"\n📊 Evidence Availability:")
    print(f"   Available: {len(summary['available'])} sources")
    for s in summary['available']:
        print(f"      ✅ {s}")
    print(f"   Unavailable: {len(summary['unavailable'])} sources")
    for s in summary['unavailable']:
        print(f"      ❌ {s}")
    print(f"\n   Note: Claims requiring unavailable evidence → NOT_VERIFIABLE")

    # Load opportunities
    opportunities = load_opportunities()
    print(f"\n📊 Found {len(opportunities)} opportunities")

    # Process sample first (10 opportunities)
    sample_size = min(10, len(opportunities))
    print(f"\n🔍 Processing {sample_size} sample opportunities first...")
    print("=" * 70)

    sample_results = []

    for opp in opportunities[:sample_size]:
        opp_name = opp["Name"]
        note_text = opp["Description"]

        # Extract claims
        claims = extract_claims_v2(note_text)

        # Evaluate claims
        result = evaluate_note(claims, opp)

        sample_results.append({
            "opp_name": opp_name,
            "amount": opp["Amount"],
            "stage": opp["StageName"],
            "claims": claims,
            "result": result
        })

        print(f"\n📋 {opp_name[:40]} (${opp['Amount']:,.0f})")
        print(f"   Stage: {opp['StageName']}")
        print(f"   Claims extracted: {len(claims)}")

        if claims:
            for claim in claims:
                claim_type = claim.get("claim_type", "unknown")
                normalized = claim.get("normalized_claim", "")[:60]
                print(f"      - {claim_type}: {normalized}")

        print(f"   Overall Decision: {result['overall_state']}")
        print(f"   Confidence: {result['overall_confidence']:.0%}")

        # Show per-claim evaluation
        if result.get('claim_results'):
            for cr in result['claim_results']:
                eval_data = cr['evaluation']
                claim_type = cr['claim'].get('claim_type', 'unknown')
                state = eval_data.get('state', 'UNKNOWN')
                reason = eval_data.get('reason', 'No reason')
                print(f"      - {claim_type}: {state} ({reason})")

    # Ask if user wants to process all 120
    print("\n" + "=" * 70)
    response = input("✅ Sample complete. Process all 120 opportunities? (y/n): ")

    if response.lower() == 'y':
        print("\n🔍 Processing all 120 opportunities...")
        print("=" * 70)

        all_results = []
        summary_stats = {
            "CONTRADICTS": 0,
            "SUPPORTED": 0,
            "UNSUPPORTED": 0,
            "NOT_VERIFIABLE": 0,
            "INSUFFICIENT": 0
        }

        for opp in opportunities:
            note_text = opp["Description"]
            claims = extract_claims_v2(note_text)
            result = evaluate_note(claims, opp)

            summary_stats[result['overall_state']] = summary_stats.get(result['overall_state'], 0) + 1

            all_results.append({
                "opp_name": opp["Name"],
                "amount": opp["Amount"],
                "stage": opp["StageName"],
                "claims": claims,
                "result": result
            })

        # Summary
        print("\n" + "=" * 70)
        print("📊 FINAL SUMMARY - ALL 120 OPPORTUNITIES")
        print("=" * 70)
        total = sum(summary_stats.values())
        print(f"Total opportunities: {total}")
        for state, count in summary_stats.items():
            if count > 0:
                pct = (count / total * 100) if total > 0 else 0
                print(f"   {state}: {count} ({pct:.1f}%)")

        # Save results
        with open("v2_results_summary.txt", "w", encoding="utf-8") as f:
            f.write("REVENUE DECISION INTEGRITY - V2 RESULTS\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total opportunities: {total}\n")
            for state, count in summary_stats.items():
                if count > 0:
                    pct = (count / total * 100) if total > 0 else 0
                    f.write(f"{state}: {count} ({pct:.1f}%)\n")
            f.write("\n" + "=" * 70 + "\n")
            f.write("CLAIM-EVIDENCE EVALUATION\n")
            f.write("-" * 50 + "\n")
            for result in all_results:
                if result['result']['claim_results']:
                    f.write(f"\n{result['opp_name'][:50]} (${result['amount']:,.0f})\n")
                    f.write(f"  Decision: {result['result']['overall_state']}\n")
                    for cr in result['result']['claim_results']:
                        claim = cr['claim']
                        eval_data = cr['evaluation']
                        f.write(f"    - {claim.get('claim_type')}: {eval_data.get('state')}\n")
                        if eval_data.get('evidence_found'):
                            f.write(f"      Evidence: {', '.join(eval_data['evidence_found'])}\n")
                        if eval_data.get('missing_sources'):
                            f.write(f"      Missing: {', '.join(eval_data['missing_sources'])}\n")

        print("\n📄 Detailed results saved to v2_results_summary.txt")

    print("\n" + "=" * 70)
    print("📋 NEXT STEPS")
    print("=" * 70)
    print("1. Review sample results to validate extraction quality")
    print("2. Review full results for classification patterns")
    print("3. Compare v1 vs v2 classifications")
    print("4. Prepare for genuine human review")


if __name__ == "__main__":
    main()