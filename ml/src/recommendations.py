def generate_training_recommendation(safety_result, anomaly_result=None):
    """
    Map detected issues to training modules.
    Input: results from safety engine and anomaly detection.
    Output: list of recommended training modules.
    """
    recommendations = []
    
    # Check safety reasons
    reasons = safety_result.get("reasons", [])
    
    if "Seatbelt Violation" in reasons:
        recommendations.append({
            "title": "Seatbelt Safety Training",
            "category": "Safety",
            "reason": "Repeated or severe seatbelt violations detected.",
            "duration": 15,
            "priority": "High"
        })
        
    if "Excessive Idling" in reasons:
        recommendations.append({
            "title": "Efficient Machine Operation",
            "category": "Efficiency",
            "reason": "Excessive machine idling time detected.",
            "duration": 30,
            "priority": "Medium"
        })
        
    if "Safety Incident Alerted" in reasons:
        recommendations.append({
            "title": "Safe Machine Operation",
            "category": "Safety",
            "reason": "Safety incidents triggered during operation.",
            "duration": 45,
            "priority": "High"
        })
        
    # Check anomaly result
    if anomaly_result and anomaly_result.get("anomaly"):
        recommendations.append({
            "title": "Machine Handling & Safety",
            "category": "Operations",
            "reason": f"Abnormal operating pattern detected ({anomaly_result.get('reason')}).",
            "duration": 60,
            "priority": "Medium"
        })
        
    return recommendations
