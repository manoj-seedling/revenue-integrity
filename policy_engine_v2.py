"""
Policy Engine V2 - Evidence-Aware Evaluation
- Sentiment claims are returned as CONTEXT_ONLY
- Overall state uses severity priority: CONTRADICTED > UNSUPPORTED > NOT_VERIFIABLE > SUPPORTED
- Handles multiple claims per opportunity
"""

from evidence_registry import (
    EVIDENCE_CAPABILITY,
    CLAIM_EVIDENCE_REQUIREMENTS,
    is_evidence_available,
    get_missing_sources
)
from datetime import datetime


def evaluate_claim(claim, opp_data):
    """
    Evaluate a single claim against available evidence.
    Returns: {state, confidence, reason, evidence_checked}
    """
    claim_type = claim.get("claim_type")
    if not claim_type:
        return {
            "state": "NOT_VERIFIABLE",
            "confidence": 0.0,
            "reason": "No claim type specified",
            "evidence_checked": []
        }

    # --- SPECIAL CASE: Sentiment is context-only ---
    if claim_type == "sentiment":
        return {
            "state": "CONTEXT_ONLY",
            "confidence": 0.0,
            "reason": "Sentiment is contextual, not evidence-based",
            "evidence_checked": [],
            "evidence_found": [],
            "evidence_gaps": [],
            "missing_sources": []
        }

    # Get evidence requirements
    requirements = CLAIM_EVIDENCE_REQUIREMENTS.get(claim_type)
    if not requirements:
        return {
            "state": "NOT_VERIFIABLE",
            "confidence": 0.0,
            "reason": f"Unknown claim type: {claim_type}",
            "evidence_checked": []
        }

    required_sources = requirements.get("required", [])
    fallback = requirements.get("fallback", "NOT_VERIFIABLE")

    # Check if required evidence sources are available
    missing = [s for s in required_sources if not EVIDENCE_CAPABILITY.get(s, False)]

    if missing:
        return {
            "state": "NOT_VERIFIABLE",
            "confidence": 0.3,
            "reason": f"Required evidence sources unavailable: {', '.join(missing)}",
            "evidence_checked": required_sources,
            "missing_sources": missing
        }

    # --- Evidence Checking (based on what's available) ---
    evidence_found = []
    evidence_gaps = []

    # Check current stage (available)
    if "current_stage" in required_sources or "stage_history" in required_sources:
        current_stage = opp_data.get("StageName", "")
        if current_stage and current_stage != "Prospecting":
            evidence_found.append(f"Current stage: {current_stage}")
        else:
            evidence_gaps.append("No meaningful stage progression")

    # Check close date (available)
    if "current_close_date" in required_sources or "close_date_history" in required_sources:
        close_date = opp_data.get("CloseDate", "")
        if close_date:
            try:
                close_date_obj = datetime.strptime(close_date, "%Y-%m-%d")
                days_to_close = (close_date_obj - datetime.now()).days
                if days_to_close > 0:
                    evidence_found.append(f"Close date set to {close_date_obj.strftime('%Y-%m-%d')}")
                else:
                    evidence_gaps.append("Close date has passed")
            except:
                evidence_found.append(f"Close date: {close_date}")
        else:
            evidence_gaps.append("No close date set")

    # Check next step text (available)
    if "next_step_text" in required_sources:
        next_step = opp_data.get("NextStep", "")
        if next_step and next_step.strip():
            evidence_found.append(f"Next step: {next_step}")
        else:
            evidence_gaps.append("No next step documented")

    # Determine final state
    if evidence_found:
        # Has some supporting evidence
        if len(evidence_gaps) >= len(evidence_found):
            # More gaps than supporting evidence
            state = "UNSUPPORTED"
            confidence = 0.4
            reason = f"Partial evidence found but {len(evidence_gaps)} gaps exist"
        else:
            state = "SUPPORTED"
            confidence = 0.75
            reason = "Supporting evidence found"
    else:
        # No supporting evidence
        state = "UNSUPPORTED"
        confidence = 0.3
        reason = "No supporting evidence found"

    # Additional: if claim is close_timeline and close date exists, it's supported
    if claim_type == "close_timeline" and opp_data.get("CloseDate"):
        state = "SUPPORTED"
        confidence = 0.80
        reason = "Close date is documented"

    return {
        "state": state,
        "confidence": confidence,
        "reason": reason,
        "evidence_checked": required_sources,
        "evidence_found": evidence_found,
        "evidence_gaps": evidence_gaps,
        "missing_sources": []
    }


def evaluate_note(claims, opp_data):
    """
    Evaluate all claims from a note and return consolidated results.
    Uses severity-based priority for overall state.
    """
    results = []
    for claim in claims:
        eval_result = evaluate_claim(claim, opp_data)
        results.append({
            "claim": claim,
            "evaluation": eval_result
        })

    # Determine overall decision using severity priority:
    # CONTRADICTED > UNSUPPORTED > NOT_VERIFIABLE > SUPPORTED
    states = [r["evaluation"]["state"] for r in results]
    if "CONTRADICTED" in states:
        overall_state = "CONTRADICTED"
    elif "UNSUPPORTED" in states:
        overall_state = "UNSUPPORTED"
    elif "NOT_VERIFIABLE" in states:
        overall_state = "NOT_VERIFIABLE"
    elif "SUPPORTED" in states:
        overall_state = "SUPPORTED"
    else:
        overall_state = "INSUFFICIENT"

    # Confidence: average of claim confidences (ignore CONTEXT_ONLY)
    confidences = [r["evaluation"]["confidence"] for r in results
                   if r["evaluation"]["state"] != "CONTEXT_ONLY"]
    overall_confidence = sum(confidences) / len(confidences) if confidences else 0.5

    return {
        "overall_state": overall_state,
        "overall_confidence": overall_confidence,
        "claims_evaluated": len(results),
        "claim_results": results
    }


def get_available_summary():
    """Return a summary of available evidence sources."""
    available = [k for k, v in EVIDENCE_CAPABILITY.items() if v]
    unavailable = [k for k, v in EVIDENCE_CAPABILITY.items() if not v]
    return {
        "available": available,
        "unavailable": unavailable,
        "note": "NOT_VERIFIABLE will be returned when required evidence is unavailable"
    }


# Quick test
if __name__ == "__main__":
    print("=" * 70)
    print("📋 POLICY ENGINE V2 - EVIDENCE AWARENESS CHECK")
    print("=" * 70)

    summary = get_available_summary()
    print(f"\nAvailable evidence: {len(summary['available'])} sources")
    for s in summary['available']:
        print(f"   ✅ {s}")
    print(f"\nUnavailable evidence: {len(summary['unavailable'])} sources")
    for s in summary['unavailable']:
        print(f"   ❌ {s}")

    print("\n" + "=" * 70)
    print("📋 CLAIM-EVIDENCE MAPPING")
    print("=" * 70)

    for claim_type, requirements in CLAIM_EVIDENCE_REQUIREMENTS.items():
        required = requirements.get("required", [])
        available = [r for r in required if EVIDENCE_CAPABILITY.get(r, False)]
        missing = [r for r in required if r not in available]
        status = "✅" if not missing else "⚠️"
        print(f"{status} {claim_type}: Available: {available}, Missing: {missing}")

    # Test a sentiment claim
    test_claim = {"claim_type": "sentiment"}
    result = evaluate_claim(test_claim, {})
    print(f"\n🧪 Sentiment test: {result['state']} (should be CONTEXT_ONLY)")

    print("\n✅ Policy Engine V2 ready.")