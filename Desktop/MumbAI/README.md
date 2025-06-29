# AI Bank Simulation City (Venice)

## Overview

AI Bank Simulation City is an interactive simulation platform that models a city's banking ecosystem using AI-driven policy decisions. The simulation leverages agent-based modeling and integrates with OpenAI's GPT-4 to dynamically generate daily underwriting policies, balancing risk and growth. The project features a Streamlit dashboard for visualization and analytics.

---

## Features
- **Agent-Based Simulation:** Models citizens with varying income, credit scores, and personalities.
- **AI Policy Agent:** Uses GPT-4 to generate daily loan approval policies based on macroeconomic and behavioral data.
- **Interactive Dashboard:** Visualizes simulation results, approval/default rates, and policy impacts.
- **Customizable Parameters:** Adjust number of agents, interest rates, and simulation days.
- **Analytics:** Track daily/cumulative approvals, defaults, and risk metrics.

---

## Directory Structure
```
Desktop/MumbAI/
  city_simulation.py      # Agent-based simulation logic
  config.yaml             # Default simulation configuration
  dashboard.py            # Streamlit dashboard app
  policy_agent_gpt.py     # GPT-4 policy agent integration
  run_simulation.py       # CLI simulation runner
  README.md               # Project documentation
```

---

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up OpenAI API Key
Create a `.env` file in `Desktop/MumbAI/` with:
```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Run the Dashboard
```bash
streamlit run Desktop/MumbAI/dashboard.py
```

### 4. Run a Simulation from CLI
```bash
python Desktop/MumbAI/run_simulation.py
```

---

## Configuration
Edit `Desktop/MumbAI/config.yaml` to set default simulation parameters:
```yaml
simulation_days: 30
num_agents: 200
starting_interest_rate: 8.5
```

---

## How It Works

### Simulation Model
- **CitizenAgent:** Each agent has random income ($2,000–$10,000), credit score (500–800), and personality (disciplined, moderate, impulsive).
- **CityModel:** Manages all agents and simulates daily loan applications and defaults.
- **Default Risk:** Influenced by interest rate and personality (impulsive agents have higher risk).

### AI Policy Agent
- **policy_agent_gpt.py:** Calls GPT-4 to generate a JSON policy with:
  - `min_credit_score`
  - `min_income`
  - `deny_if_personality` (e.g., ["impulsive"])
  - `reason` (explanation for the policy)
- **Error Handling:** If the API response is not valid JSON, the simulation halts and prints an error.

### Dashboard Features
- **Sidebar Controls:** Adjust simulation parameters interactively.
- **Key Metrics:** Total approvals, defaults, approval/default rates.
- **Charts:** Daily trends, cumulative totals, and policy summary.
- **Raw Data:** View daily simulation results in a table.

---

## Example Policy (from GPT-4)
```json
{
  "min_credit_score": 690,
  "min_income": 4800,
  "deny_if_personality": ["impulsive"],
  "reason": "To balance portfolio growth and mitigate elevated NPA risk (5.3%), we set moderately high requirements. Applicants with 'impulsive' personality score are denied due to significantly higher default probability (0.14). Lower threshold for income is set close to average (5200) to allow reasonable portfolio growth, while credit score is kept above average to control NPA risk."
}
```

---

## Troubleshooting
- **API Response Errors:** If you see `JSONDecodeError` or `Policy is None`, check your OpenAI API key and ensure the API returns valid JSON.
- **Dependencies:** Ensure all packages in `requirements.txt` are installed.

---

## Dependencies
Key packages (see `requirements.txt` for full list):
- `streamlit`, `plotly`, `pandas`, `mesa`, `openai`, `python-dotenv`

---

## License
MIT License. See [LICENSE](../LICENSE) if available.

---

## Acknowledgments
- Powered by [Mesa](https://mesa.readthedocs.io/) for agent-based modeling
- [Streamlit](https://streamlit.io/) for the dashboard
- [OpenAI GPT-4](https://platform.openai.com/) for policy generation
