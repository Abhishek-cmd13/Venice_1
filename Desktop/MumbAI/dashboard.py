import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
from city_simulation import CityModel
from run_simulation import simulate_day
from policy_agent_gpt import get_daily_policy
import traceback

# Page config
st.set_page_config(
    page_title="AI Bank Simulation City",
    page_icon="🏦",
    layout="wide"
)

# Title and description
st.title("🏦 AI Bank Simulation City")
st.markdown("**Interactive AI-powered banking simulation with dynamic policy decisions**")

# Sidebar controls
st.sidebar.header("🎛️ Simulation Controls")

# Simulation parameters
num_agents = st.sidebar.slider("Number of Citizens", 50, 500, 200, step=50)
interest_rate = st.sidebar.slider("Interest Rate (%)", 1.0, 15.0, 8.5, step=0.5)
simulation_days = st.sidebar.slider("Simulation Days", 1, 30, 7, step=1)

# OpenAI API Key
# st.sidebar.header("🔑 OpenAI API Key")
# api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

# Run simulation button
if st.sidebar.button("🚀 Run Simulation", type="primary"):
    # Removed API key check since it's hardcoded in policy_agent_gpt.py
    try:
        with st.spinner("Running AI Bank Simulation..."):
            # Initialize model
            model = CityModel(num_agents=num_agents, interest_rate=interest_rate)
            
            # Prepare dummy data for GPT-4
            dummy_data = {
                "interest_rate": interest_rate,
                "npa_rate": 5.3,  # Example NPA rate
                "avg_income": 5200,  # Example average income
                "personality_risk": {
                    "disciplined": 0.01,
                    "moderate": 0.06,
                    "impulsive": 0.14
                }
            }
            
            # Get policy from GPT-4
            policy = get_daily_policy(dummy_data)

            # Check if policy is None
            if policy is None:
                print("Error: Policy is None. Check API response.")
                st.error("Error: Policy is None. Check API response.")
                raise st.StopException()
            
            # Run simulation
            results = []
            daily_stats = []
            
            for day in range(simulation_days):
                model.step()
                approved, defaults = simulate_day(model, policy)
                
                # Collect daily stats
                total_agents = len(model.agents)
                applied_today = sum(1 for agent in model.agents if agent.applied_today)
                total_approved = sum(1 for agent in model.agents if agent.approved)
                total_defaults = sum(1 for agent in model.agents if agent.defaulted)
                
                daily_stats.append({
                    "Day": day + 1,
                    "Applied": applied_today,
                    "Approved": approved,
                    "Defaults": defaults,
                    "Total_Approved": total_approved,
                    "Total_Defaults": total_defaults,
                    "Approval_Rate": (approved / applied_today * 100) if applied_today > 0 else 0,
                    "Default_Rate": (defaults / total_approved * 100) if total_approved > 0 else 0
                })
            
            # Create results dataframe
            df_daily = pd.DataFrame(daily_stats)
            
            # Display results
            st.success(f"✅ Simulation completed! {simulation_days} days simulated with {num_agents} citizens.")
            
            # Key metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Approvals", f"{df_daily['Approved'].sum():,}")
            with col2:
                st.metric("Total Defaults", f"{df_daily['Defaults'].sum():,}")
            with col3:
                avg_approval_rate = df_daily['Approval_Rate'].mean()
                st.metric("Avg Approval Rate", f"{avg_approval_rate:.1f}%")
            with col4:
                avg_default_rate = df_daily['Default_Rate'].mean()
                st.metric("Avg Default Rate", f"{avg_default_rate:.1f}%")
            
            # Charts
            st.subheader("📊 Simulation Analytics")
            
            # Daily trends
            col1, col2 = st.columns(2)
            
            with col1:
                fig_approvals = px.line(df_daily, x='Day', y=['Applied', 'Approved', 'Defaults'], 
                                      title="Daily Loan Activity", markers=True)
                fig_approvals.update_layout(height=400)
                st.plotly_chart(fig_approvals, use_container_width=True)
            
            with col2:
                fig_rates = px.line(df_daily, x='Day', y=['Approval_Rate', 'Default_Rate'], 
                                   title="Approval & Default Rates (%)", markers=True)
                fig_rates.update_layout(height=400)
                st.plotly_chart(fig_rates, use_container_width=True)
            
            # Cumulative totals
            fig_cumulative = px.line(df_daily, x='Day', y=['Total_Approved', 'Total_Defaults'], 
                                    title="Cumulative Approvals vs Defaults", markers=True)
            fig_cumulative.update_layout(height=400)
            st.plotly_chart(fig_cumulative, use_container_width=True)
            
            # Policy summary
            st.subheader("📋 Applied Policy")
            st.info(f"""
            **Policy Applied:**
            - Minimum Credit Score: {policy['min_credit_score']}
            - Minimum Income: ${policy['min_income']:,}
            - Deny Impulsive: {'Yes' if 'impulsive' in policy['deny_if_personality'] else 'No'}
            - Reason: {policy['reason']}
            """)
            
            # Raw data
            st.subheader("📈 Detailed Results")
            st.dataframe(df_daily, use_container_width=True)
    except Exception as e:
        print("[ERROR] Exception during simulation run:")
        traceback.print_exc()
        st.error(f"[ERROR] Exception during simulation run: {e}")

# Default state
else:
    st.info("👈 Use the sidebar controls to configure and run your AI bank simulation!")
    
    # Show sample data structure
    st.subheader("📋 Sample Simulation Structure")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Citizen Agents:**")
        st.markdown("""
        - Income: $2,000 - $10,000
        - Credit Score: 500 - 800
        - Personalities: Disciplined, Moderate, Impulsive
        - 30% daily loan application rate
        """)
    
    with col2:
        st.markdown("**Policy Decisions:**")
        st.markdown("""
        - Credit score thresholds
        - Income requirements
        - Personality-based restrictions
        - Risk-based default modeling
        """)
    
    st.markdown("---")
    st.markdown("**🎯 Ready to simulate your AI-powered banking city!**")

# Footer
st.markdown("---")
st.markdown("*AI Bank Simulation City - Powered by Mesa & Streamlit*")