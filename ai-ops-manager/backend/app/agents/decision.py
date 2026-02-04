def decide_action(intent: str):
    mapping = {

        "sales": "update_crm_and_reply",
        "support" : "create_ticket_and_reply",
        "billing" : "escallate_billing",
        "onboarding" : "start_onboarding_flow"
    }
    return mapping.get(intent, "manual_review")