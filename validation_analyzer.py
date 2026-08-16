"""Analyze completed Phase 2 manager-validation CSV files.

Run from the directory containing claims.csv, reviews.csv, and adjudication.csv:
    python validation_analyzer.py

This reports reviewer acceptance and agreement on surfaced synthetic cases.
It does not calculate recall or real-world precision.
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent

ALLOWED = {
    "Claim_Detection_Correct": {"YES", "NO", "PARTIAL"},
    "Evidence_Policy_Appropriate": {"YES", "NO", "CANNOT_DETERMINE"},
    "Proposed_State_Correct": {"YES", "NO", "CANNOT_DETERMINE"},
    "Business_Useful": {"YES", "NO", "UNSURE"},
}


def read_csv(name):
    with (ROOT / name).open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def normalized(value):
    return (value or "").strip().upper()


claims = read_csv("claims.csv")
reviews = read_csv("reviews.csv")
claim_ids = {row["Claim_ID"] for row in claims}

if len(claims) != 13 or len(claim_ids) != 13:
    raise ValueError("Expected 13 unique claims in claims.csv")
if len(reviews) != 26:
    raise ValueError("Expected 26 review rows: 13 claims x 2 reviewers")

errors = []
for row_number, row in enumerate(reviews, start=2):
    if row.get("Claim_ID") not in claim_ids:
        errors.append(f"Row {row_number}: unknown Claim_ID {row.get('Claim_ID')!r}")
    confidence = (row.get("Reviewer_Confidence") or "").strip()
    if confidence and confidence not in {"1", "2", "3", "4", "5"}:
        errors.append(f"Row {row_number}: Reviewer_Confidence must be 1-5")
    for field, allowed in ALLOWED.items():
        value = normalized(row.get(field))
        if value and value not in allowed:
            errors.append(f"Row {row_number}: invalid {field} value {value!r}")

if errors:
    raise ValueError("Invalid review data:\n- " + "\n- ".join(errors))

completed = [r for r in reviews if normalized(r.get("Claim_Detection_Correct"))]
print("REVENUE DECISION INTEGRITY - VALIDATION SUMMARY")
print("=" * 56)
print(f"Claims: {len(claims)} across {len({c['Case_ID'] for c in claims})} opportunities")
print(f"Review assignments completed: {len(completed)}/{len(reviews)}")

if not completed:
    print("\nNo completed reviews yet. The templates are ready for independent review.")
    raise SystemExit(0)

for reviewer in sorted({r["Reviewer_ID"] for r in reviews}):
    rows = [r for r in completed if r["Reviewer_ID"] == reviewer]
    print(f"\n{reviewer}: {len(rows)}/13 completed")
    for field in ALLOWED:
        counts = Counter(normalized(r.get(field)) for r in rows if normalized(r.get(field)))
        rendered = ", ".join(f"{key}={value}" for key, value in sorted(counts.items())) or "none"
        print(f"  {field}: {rendered}")

by_claim = defaultdict(list)
for review in completed:
    by_claim[review["Claim_ID"]].append(review)

agreement_fields = list(ALLOWED)
print("\nINTER-REVIEWER AGREEMENT")
for field in agreement_fields:
    comparable = 0
    matches = 0
    for rows in by_claim.values():
        values = [normalized(r.get(field)) for r in rows if normalized(r.get(field))]
        if len(values) == 2:
            comparable += 1
            matches += values[0] == values[1]
    rate = f"{matches / comparable * 100:.1f}%" if comparable else "pending"
    print(f"  {field}: {matches}/{comparable} ({rate})")

reason_counts = Counter(
    normalized(r.get("Primary_Reason_Code"))
    for r in completed
    if normalized(r.get("Primary_Reason_Code"))
)
print("\nREASON CODES")
if reason_counts:
    for reason, count in reason_counts.most_common():
        print(f"  {reason}: {count}")
else:
    print("  None recorded")

print("\nInterpretation: preliminary reviewer acceptance on surfaced synthetic cases;")
print("not recall, independently validated real-world precision, or commercial impact.")
