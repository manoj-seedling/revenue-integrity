# Revenue Decision Integrity Engine

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![Status](https://img.shields.io/badge/Status-MVP%20Complete-brightgreen)]()
[![Cost](https://img.shields.io/badge/Cost-$0-success)]()

> *"An AI-powered evidence reconciliation engine that tests seller claims against CRM evidence—and knows what it cannot test."*

---

## The Problem

Sales Operations spends 45+ minutes per deal manually reconciling rep narratives against CRM evidence. Forecast calls become debates about "what the rep said" vs "what the data shows."

**The three recurring questions:**
1. What changed?
2. Why did it change?
3. Can we trust it?

**The challenge:** The information exists; the decision-ready evidence does not.

---

## The Solution

A zero-cost evidence reconciliation engine that:

- ✅ Extracts granular claims from rep notes using LLM
- ✅ Tests claims against CRM evidence using deterministic rules
- ✅ Explicitly identifies when evidence is unavailable (`NOT_VERIFIABLE`)
- ✅ Returns auditable, transparent decision states
- ✅ Costs $0 (Open Source + Groq Free Tier)

**The principle:** *Evidence before intervention. No recommendation becomes an operating instruction until the system shows the supporting evidence, the confidence level, and what would disconfirm the conclusion.*

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           REP NOTE                                        │
│  "Champion is engaged. Legal review next week. Budget approved."           │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LLM EXTRACTION (Granular)                              │
│  Claim 1: champion_engaged    → "Champion is engaged"                      │
│  Claim 2: legal_process_active → "Legal review in progress"                │
│  Claim 3: budget_approved     → "Budget approved"                          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      EVIDENCE REGISTRY                                    │
│  Explicitly states which evidence sources are available                   │
│  If source missing → NOT_VERIFIABLE                                      │
│  If source empty    → UNSUPPORTED                                        │
│  If evidence matches → SUPPORTED                                         │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                       DECISION STATE                                      │
│  SUPPORTED     → Claim + Evidence match                                   │
│  UNSUPPORTED   → Claim exists, evidence missing                           │
│  CONTRADICTED  → Evidence conflicts with claim                            │
│  NOT_VERIFIABLE → Required evidence source unavailable                    │
│  CONTEXT_ONLY  → Sentiment claims (contextual only)                      │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        HUMAN REVIEW                                       │
│  Validate, Dismiss, or Reclassify—preserving expert judgment            │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Language** | Python 3.x | Core logic and orchestration |
| **LLM** | Groq (`llama-3.3-70b-versatile`) | Granular claim extraction |
| **Environment** | Virtualenv | Dependency isolation |
| **Data Source** | CSV (Salesforce export) | 120 sample opportunities |
| **Security** | `python-dotenv` | Secure API key management |

---

## Key Results

### V1 vs V2 Comparison

| Metric | V1 | V2 | Change |
|--------|-----|-----|--------|
| **CONTRADICTS** | 12 | 0 | **-12 ✅** |
| **NOT_VERIFIABLE** | 0 | 52 | **+52 ✅** |
| **SUPPORTED** | 0 | 0 | 0 |
| **INSUFFICIENT** | 108 | 68 | **-40 ✅** |

### Interpretation

- ✅ **52 NOT_VERIFIABLE:** The system correctly identifies claims that cannot be tested due to missing evidence sources.
- ✅ **12 CONTRADICTS removed:** V2 stopped misclassifying unsupported claims as contradictions.
- ✅ **40 INSUFFICIENT reduced:** Claims were successfully extracted from 40 more opportunities.

**Key Insight:** *The system knows what it cannot test—which is more valuable than testing incorrectly.*

---

## Evidence Registry

| Source | Available? | Notes |
|--------|------------|-------|
| `current_stage` | ✅ Yes | From CSV |
| `current_close_date` | ✅ Yes | From CSV |
| `next_step_text` | ✅ Yes | From CSV |
| `description_text` | ✅ Yes | From CSV |
| `tasks` | ❌ No | Not in CSV |
| `events` | ❌ No | Not in CSV |
| `contacts` | ❌ No | Not in CSV |
| `stage_history` | ❌ No | Not in CSV |
| `close_date_history` | ❌ No | Not in CSV |
| `approval_records` | ❌ No | Not in CSV |

---

## Project Structure

```
revenue-integrity/
├── README.md                    # This file
├── LICENSE                      # MIT License
├── requirements.txt             # Python dependencies
├── .env.example                 # Example environment variables
├── .gitignore                   # Git ignore rules
│
├── evidence_registry.py         # Evidence capability registry
├── llm_extractor_v2.py          # Granular LLM-based claim extraction
├── policy_engine_v2.py          # Registry-aware evidence evaluation
├── run_policy_v2.py             # Complete pipeline runner
├── compare_v1_v2.py             # V1 vs V2 comparison
│
├── opportunities.csv            # Sample data (120 records)
└── v2_results_summary.txt       # Final V2 results
```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/manoj-seedling/revenue-integrity.git
cd revenue-integrity
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
cp .env.example .env
# Edit .env with your GROQ_API_KEY
```

### 5. Run the Pipeline

```bash
python run_policy_v2.py
```

---

## Requirements

```
python-dotenv==1.0.1
groq==0.9.0
requests==2.31.0
```

---

## Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **LLM for extraction only** | Separates concerns: AI understands language, rules validate evidence |
| **Evidence registry** | Explicitly states what can and cannot be tested |
| **NOT_VERIFIABLE state** | Honest AI: system knows its limitations |
| **No write-back** | Preserves human judgment as the final decision point |
| **$0 cost** | Proves enterprise solutions don't require enterprise budgets |

---

## Limitations & Next Steps

| Limitation | Mitigation |
|------------|------------|
| Synthetic data | Validate on live Salesforce data |
| Missing evidence sources | Add tasks, contacts, stage history |
| Rate limits | Switch to `llama-3.1-8b-instant` or upgrade tier |
| Recall not measured | Blind review sample needed |
| Simulated human reviewers | Conduct real manager validation |

---

## License

MIT License — feel free to use, modify, and distribute.

---

## Author

**Manojkumar Nithyanantham**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue)](https://linkedin.com/in/your-profile)

---

## One-Sentence Summary

> *"We built a zero-cost evidence reconciliation engine that detects contradictions between seller claims and CRM evidence, correctly identifies when evidence is unavailable, and provides auditable, transparent decision states—proving that honest AI systems can deliver enterprise value without expensive infrastructure."*

---

## Acknowledgments

- **Groq** for providing a free LLM tier
- **Salesforce** for the Developer Edition
- **Workbench** for data management and export

---

## How to Contribute

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## Support

For questions or feedback, please open an issue or reach out directly.

---

**Built with ❤️ for Sales Ops and Revenue Operations professionals.**