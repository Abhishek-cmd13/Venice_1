from city_simulation import CityModel
from policy_agent_gpt import get_daily_policy

def simulate_day(model, policy):
    approved, defaults = 0, 0
    for agent in model.agents:
        if agent.applied_today:
            if (agent.credit_score >= policy['min_credit_score']
                and agent.income >= policy['min_income']
                and agent.personality not in policy['deny_if_personality']):
                agent.approved = True
                approved += 1
            else:
                agent.approved = False
        if agent.defaulted:
            defaults += 1
    return approved, defaults

if __name__ == "__main__":
    import traceback
    try:
        model = CityModel(num_agents=200, interest_rate=8.5)
        dummy_data = {
            "interest_rate": model.interest_rate,
            "npa_rate": 5.3,
            "avg_income": 5200,
            "personality_risk": {
                "disciplined": 0.01,
                "moderate": 0.06,
                "impulsive": 0.14
            }
        }
        policy = {
            "min_credit_score": 650,
            "min_income": 4000,
            "deny_if_personality": ["impulsive"],
            "reason": "Default risk is high due to current macro conditions."
        }
        model.step()
        approved, defaults = simulate_day(model, policy)
        print(f"Day {model.day}: Approved: {approved}, Defaults: {defaults}")
    except Exception as e:
        print("[ERROR] An exception occurred during simulation:")
        traceback.print_exc()