"""
Evidence Capability Registry
Explicitly states which evidence sources are available in the current dataset.
"""

EVIDENCE_CAPABILITY = {
    # From opportunities.csv - Available
    "current_stage": True,
    "current_close_date": True,
    "next_step_text": True,
    "description_text": True,
    
    # Not available in current CSV
    "tasks": False,
    "events": False,
    "contacts": False,
    "contact_roles": False,
    "stage_history": False,
    "close_date_history": False,
    "dated_next_steps": False,
    "approval_records": False,
    "legal_events": False,
    "email_messages": False,
    "call_logs": False,
    "activity_dates": False,
}

# Claim types mapped to required evidence sources
CLAIM_EVIDENCE_REQUIREMENTS = {
    "champion_engaged": {
        "required": ["contacts", "tasks", "events"],
        "fallback": "NOT_VERIFIABLE"
    },
    "deal_momentum": {
        "required": ["stage_history", "tasks", "events"],
        "fallback": "NOT_VERIFIABLE"
    },
    "decision_maker_support": {
        "required": ["contacts", "events"],
        "fallback": "NOT_VERIFIABLE"
    },
    "budget_approved": {
        "required": ["approval_records"],
        "fallback": "NOT_VERIFIABLE"
    },
    "blocker_absence": {
        "required": ["tasks", "events", "next_step_text"],
        "fallback": "NOT_VERIFIABLE"
    },
    "legal_process_active": {
        "required": ["legal_events", "tasks", "contacts"],
        "fallback": "NOT_VERIFIABLE"
    },
    "close_timeline": {
        "required": ["close_date_history"],
        "fallback": "NOT_VERIFIABLE"
    },
    "sentiment": {
        "required": [],
        "fallback": "CONTEXT_ONLY"
    }
}

# Claim type definitions for the LLM prompt
CLAIM_TAXONOMY_V2 = """
1. champion_engaged: Rep states a champion is actively engaged and supportive.
   - Required evidence: Contact + recent activity (tasks/events)
   - Example: "Sarah is fully bought in", "Champion is engaged"

2. deal_momentum: Rep states the deal is progressing well and moving forward.
   - Required evidence: Stage progression + recent activity
   - Example: "Deal is on track", "Everything is green", "Strong momentum"

3. decision_maker_support: Rep states a decision maker is supportive.
   - Required evidence: Documented interaction or attributed statement
   - Example: "CFO is supportive", "The VP is on board"

4. budget_approved: Rep states budget has been approved.
   - Required evidence: Approval record or documented confirmation
   - Example: "Budget approved", "Funding is secured"

5. blocker_absence: Rep states no blockers exist.
   - Required evidence: Process evidence covering known risk areas
   - Example: "No blockers", "No issues", "Everything is clear"

6. legal_process_active: Rep states legal review is in progress.
   - Required evidence: Legal tasks, redline events, or legal contact
   - Example: "Legal review in progress", "Redlines exchanged"

7. close_timeline: Rep mentions a specific close date or timeframe.
   - Required evidence: Close date history
   - Example: "Close by end of quarter", "Should close next week"

8. sentiment: Overall tone of the note (positive/negative/neutral).
   - Required evidence: None (contextual only)
"""


def is_evidence_available(required_sources):
    """Check if all required evidence sources are available."""
    for source in required_sources:
        if not EVIDENCE_CAPABILITY.get(source, False):
            return False
    return True


def get_available_evidence_sources():
    """Return list of available evidence sources."""
    return [k for k, v in EVIDENCE_CAPABILITY.items() if v]


def get_missing_sources(claim_type):
    """Return missing evidence sources for a claim type."""
    requirements = CLAIM_EVIDENCE_REQUIREMENTS.get(claim_type, {}).get("required", [])
    return [s for s in requirements if not EVIDENCE_CAPABILITY.get(s, False)]

def get_available_summary():
    """Return a summary of available evidence sources."""
    available = [k for k, v in EVIDENCE_CAPABILITY.items() if v]
    unavailable = [k for k, v in EVIDENCE_CAPABILITY.items() if not v]
    return {
        "available": available,
        "unavailable": unavailable,
        "note": "NOT_VERIFIABLE will be returned when required evidence is unavailable"
    }