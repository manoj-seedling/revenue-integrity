from datetime import datetime, timedelta

class PaperweightPolicy:
    def evaluate(self, opp, tasks, history, primary_contact, note_text):
        result = {
            "decision": "INSUFFICIENT",
            "confidence": 0.5,
            "reasons": [],
            "question": None,
            "contradicting_facts": [],
            "supporting_facts": []
        }
        
        # 1. Check if there are any tasks linked to the primary contact
        if not tasks:
            result["contradicting_facts"].append("No tasks linked to buyer contact in last 30 days")
        else:
            result["supporting_facts"].append(f"Found {len(tasks)} tasks with buyer")
        
        # 2. Check close date slippage
        close_changes = [h for h in history if h.get("Field") == "CloseDate"]
        if len(close_changes) >= 2:
            result["contradicting_facts"].append(f"Close date moved {len(close_changes)} times")
        elif close_changes:
            result["supporting_facts"].append("Close date history is stable")
        
        # 3. Check if opportunity is stale
        last_act = opp.get("LastActivityDate")
        if last_act:
            try:
                last_date = datetime.strptime(last_act, "%Y-%m-%d")
                if (datetime.now() - last_date).days > 30:
                    result["contradicting_facts"].append("No activity logged in over 30 days")
                else:
                    result["supporting_facts"].append(f"Recent activity on {last_act}")
            except:
                pass
        else:
            result["contradicting_facts"].append("No LastActivityDate recorded")
        
        # 4. Check stage history
        stage_changes = [h for h in history if h.get("Field") == "StageName"]
        if not stage_changes:
            result["contradicting_facts"].append("Opportunity has never moved from current stage")
        else:
            result["supporting_facts"].append("Has had stage changes")
        
        # 5. Extract claim from note
        if note_text:
            if "engaged" in note_text.lower() or "champion" in note_text.lower():
                result["extracted_claims"] = {"champion_engaged": True}
                result["claim_source"] = note_text[:200]
                
                if len(result["contradicting_facts"]) >= 2:
                    result["decision"] = "CONTRADICTS"
                    result["confidence"] = 0.85
                    result["question"] = "Manager: Rep claims champion engagement, but CRM shows zero buyer tasks or activity in 30+ days. Please confirm."
                else:
                    result["decision"] = "INSUFFICIENT"
                    result["confidence"] = 0.5
                    result["question"] = "Claim of engagement found, but evidence is incomplete. Please update with specific buyer tasks."
            else:
                result["decision"] = "INSUFFICIENT"
                result["confidence"] = 0.3
                result["question"] = "No engagement claim found in notes. Please add status update on buyer activity."
        else:
            result["decision"] = "INSUFFICIENT"
            result["confidence"] = 0.2
            result["question"] = "No notes found. Please add a status comment."
        
        return result