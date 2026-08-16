# Revenue Decision Integrity Engine — Complete FAQ

**Audience:** Sales Ops Leaders, AI Architects, End Users
**Date:** August 16, 2026
**Version:** 1.0

---

## Section 1: Business Value

### 1. What problem does this solve?

**The Short Answer:**

Sales Operations spends 45+ minutes per deal manually reconciling rep narratives against CRM evidence. Forecast calls become debates about "what the rep said" vs "what the data shows." This system automates that reconciliation, providing auditable, evidence-backed decision support.

**The Detailed Answer:**

Before every forecast review, Sales Ops leaders ask three questions:

| Question | What Actually Happens |
|----------|----------------------|
| **What changed?** | Movement is visible, but scattered across views and systems. |
| **Why did it change?** | The explanation lives in notes, calls, or informal manager context—not in a consistent evidence trail. |
| **Can we trust it?** | A forecast can be internally plausible while being weakly supported by CRM facts and observed execution. |

**The result:** Forecast calls become debates. Time is wasted reconstructing cases that should have been obvious.

---

### 2. Can you give me a concrete scenario where this would have helped?

**Scenario: The Quarterly Forecast Review**

It's 48 hours before the Q3 forecast review. The VP of Sales Ops needs to present a credible forecast to the CFO.

**The Workflow:**
- 6 regional Sales Directors submit their forecasts
- 12 Sales Managers provide commentary
- 45 Account Executives have logged notes across 300+ opportunities

**The Problem:**

The VP pulls a report showing 40 "Commit" deals worth $18M. But when they dig deeper:

| Deal | Rep Narrative | CRM Evidence | Reality |
|------|---------------|--------------|---------|
| Acme Corp | "Champion is engaged. Legal review next week." | No activity in 45 days. No tasks. Close date slipped twice. | Rep is optimistic. No evidence of progress. |
| GlobalTech | "Budget approved. CFO is supportive." | No approval documentation. No CFO meeting logged. | Assumption. No proof. |
| MegaCorp | "Everything is green. Closing this quarter." | Stage hasn't moved in 90 days. Last activity: 60 days ago. | Deal is stalled. Rep is in denial. |

**The Cost:**
- 3 Sales Ops analysts spend **8 hours each** manually investigating 40 deals
- **24 hours of lost productivity** before the forecast review
- **$400K+ in at-risk pipeline** identified only after urgent investigation
- Trust in the forecast process erodes

**The System's Role:**

The Revenue Decision Integrity Engine would have flagged all three deals automatically:

| Deal | Flag | Evidence |
|------|------|----------|
| Acme Corp | CONTRADICTS | Claims "engaged" but no tasks, no activity, close date slipped |
| GlobalTech | NOT_VERIFIABLE | Claims "budget approved" but no approval evidence available |
| MegaCorp | UNSUPPORTED | Claims "green" but no stage progression, no recent activity |

**The Result:** The VP walks into the forecast review with a pre-validated list of exceptions, not a list of surprises.

---

### 3. What's the ROI?

| Metric | Phase 1 | Phase 2.1 |
|--------|---------|-----------|
| Contradictions Found | 12 | 52 (correctly reclassified) |
| Analyst Time Saved | ~45 min/deal | ~45 min/deal |
| Cost | $0 | $0 |
| Risk Identified | ~$400K pipeline | Correctly identified untestable claims |

The system costs $0 to run. The ROI is effectively infinite.

**The real ROI:**
- **Time saved:** 45 minutes per deal × 300 deals per quarter = 225 hours per quarter
- **Risk identified:** Deals that would have slipped without investigation
- **Forecast integrity:** Trust restored in the forecast process
- **Leadership confidence:** Evidence-backed decisions, not gut-feel

---

### 4. Why is this different from existing tools?

| Tool | What It Does | What It Misses |
|------|--------------|----------------|
| **Dashboards** | Show current state | Don't assemble cross-signal evidence |
| **Forecast Tools** | Capture submissions | Don't test claims against evidence |
| **BI Alerts** | Surface exceptions | Don't prioritize or recommend action |
| **AI Summaries** | Make text readable | Can create false confidence without evidence |

**This system tests claims, not just displays them. It separates facts from inferences.**

---

### 5. What's the biggest risk?

**Overclaiming.** The system is honest about its limitations. If required evidence sources (tasks, contacts, history) are unavailable, it returns `NOT_VERIFIABLE` rather than forcing a false positive.

**The risk is not the technology—it's using the output without human judgment.**

**Risk Mitigation:**

| Risk | Mitigation |
|------|------------|
| False positives | Human review and validation |
| Over-reliance | System is a decision-support tool, not a decision-maker |
| Data gaps | Evidence registry makes gaps explicit |
| Model drift | Regular validation and calibration |

---

### 6. When is this ready for production?

| Milestone | Status |
|-----------|--------|
| MVP Engineering Experiment | ✅ Complete |
| Simulated Validation | ✅ Complete |
| Genuine Human Validation | ⬜ Pending |
| Live Data Integration | ⬜ Pending |
| Production | ⬜ After human validation + live data |

**Current status:** MVP Engineering Experiment Complete — Independent Validation Pending.

---

## Section 2: Technical Architecture

### 7. What's the high-level architecture?
