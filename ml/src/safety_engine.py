def evaluate_safety(telemetry_data):
    """
    Evaluates safety based on deterministic rules.
    Input: dict with telemetry features.
    Output: dict with safety score, risk level, and reasons.
    """
    seatbelt_status = telemetry_data.get('seatbelt_status')
    safety_alert = telemetry_data.get('safety_alert')
    idling_time = telemetry_data.get('idling_time', 0)
    
    score = 100
    reasons = []
    
    if seatbelt_status == "Unfastened":
        score -= 30
        reasons.append("Seatbelt Violation")
        
    if safety_alert:
        score -= 40
        reasons.append("Safety Incident Alerted")
        
    if idling_time > 45:
        score -= 15
        reasons.append("Excessive Idling")
        
    if score >= 85:
        risk_level = "LOW RISK"
    elif score >= 60:
        risk_level = "MEDIUM RISK"
    else:
        risk_level = "HIGH RISK"
        
    return {
        "safety_score": max(0, score),
        "risk_level": risk_level,
        "reasons": reasons
    }
