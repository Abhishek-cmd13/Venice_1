import random
import traceback
# CitizenAgent class
class CitizenAgent:
    def __init__(self, unique_id, model):
        self.unique_id = unique_id
        self.model = model
        self.income = random.randint(2000, 10000)
        self.credit_score = random.randint(500, 800)
        self.personality = random.choice(["disciplined", "moderate", "impulsive"])
        self.applied_today = False
        self.approved = False
        self.defaulted = False

    def step(self):
        try:
            self.applied_today = random.random() < 0.3  # 30% apply for loans
            if self.approved and not self.defaulted:
                default_risk = 0.05 * self.model.interest_rate / 10
                if self.personality == "impulsive":
                    default_risk *= 2
                elif self.personality == "disciplined":
                    default_risk *= 0.5
                if random.random() < default_risk:
                    self.defaulted = True
        except Exception as e:
            print(f"[ERROR] Exception in CitizenAgent.step (agent_id={self.unique_id}):")
            traceback.print_exc()

class CityModel:
    def __init__(self, num_agents, interest_rate):
        self.num_agents = num_agents
        self.interest_rate = interest_rate
        self.agents = [CitizenAgent(i, self) for i in range(self.num_agents)]
        self.day = 0

    def step(self):
        self.day += 1
        for agent in self.agents:
            try:
                agent.step()
            except Exception as e:
                print(f"[ERROR] Exception in CityModel.step (agent_id={agent.unique_id}):")
                traceback.print_exc()