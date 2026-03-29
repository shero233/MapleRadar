import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
from datetime import datetime, timedelta


if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'user_state' not in st.session_state:
    st.session_state.user_state = {
        "available_time": 480,  # 8 hours in mins
        "energy_level": "medium",
        "stress_level": 1,
        "energy_val": 5
    }

def fetch_live_toronto_status():
    import random
    events = [
        {"type": "Weather", "desc": "Extreme Cold Alert (-20°C)", "effect": "Low_Energy", "impact": -2},
        {"type": "TTC", "desc": "Subway Line 1: Signal Issues", "effect": "2hr_Travel", "impact": -120},
        {"type": "Economic", "desc": "Loblaws 30% Price Surge", "effect": "Stress", "impact": 1}
    ]
    return random.choice(events) 

def apply_effect(chain):
    state = st.session_state.user_state
    steps = chain.split("->")
    for step in steps:
        step = step.strip()
        if "2hrs_Lost" in step or "2hr_Travel" in step:
            state["available_time"] = max(0, state['available_time'] - 120)
        elif "Long_Commute" in step or "3hr_Daily" in step:
            state["available_time"] = max(0, state["available_time"] - 180)
        elif any(k in step for k in ["Stress", "Anxiety", "Burnout", "Depression"]):
            state["energy_val"] = max(0, state["energy_val"] - 2)
            state["stress_level"] += 2
        elif "Late" in step:
            state["stress_level"] += 1
    
    
    if state["energy_val"] <= 2: state["energy_level"] = "low"
    elif state["energy_val"] >= 7: state["energy_level"] = "high"
    else: state["energy_level"] = "medium"

def score_task(task, state):
    
    days_left = max(0, (task["deadline"] - datetime.now()).days)
    urgency = 1 / (1 + days_left)
    energy_score = -0.5 if state["energy_level"] == "low" and task["energy_required"] == "high" else 0
    stress_bonus = state["stress_level"] * 0.1
    return urgency + energy_score + stress_bonus

st.set_page_config(page_title="MapleRadar", layout="wide")


st.markdown("""<style>...</style>""", unsafe_allow_html=True)


TORONTO_KNOWLEDGE_BASE = {
    # Housing & Rent
    "Housing Crisis": "Rent_+$400 -> Move_to_North_York -> 3hr_Daily_Commute -> Study_Time_Cut -> GPA_Risk",
    "Rental Scam": "Cheap_Listing_Found -> Pay_Deposit -> Ghosted_by_Landlord -> Lose_1500_CAD -> Emergency_Crisis",
    "Roommate Conflict": "Rent_Too_High -> Shared_Room -> No_Privacy -> Sleep_Deprivation -> Mental_Burnout",

    # TTC & Transit
    "TTC Service Cut": "TTC_Delay -> Late_for_Work -> Wage_Deduction -> Mental_Stress",
    "Winter Blizzard": "Heavy_Snow -> TTC_Subway_Closure -> Walk_in_Cold -> Get_Sick -> Miss_Midterm",
    "Fare Hike": "Presto_Fare_Rise -> Monthly_Budget_Tight -> Skip_Social_Events -> Social_Isolation -> Depression",

    # Cost of Living
    "Loblaws Inflation": "Loblaws_Price_Spike -> Switch_to_NoFrills -> 2hr_Travel -> Stress",
    "Food Bank Reliance": "Grocery_Cost_Rising -> Paycheck_Shortfall -> Visit_Food_Bank -> Social_Anxiety -> Mental_Burnout",
    "Hydro Bill Surge": "Winter_Heating_Cost -> Hydro_Bill_+$100 -> Cut_Food_Budget -> Poor_Nutrition -> Low_Energy",

    # Job & Academic
    "Job Market Struggle": "Fewer_Part-time_Jobs -> Credit_Card_Debt -> High_Interest -> Debt_Spiral",
    "Resume Void": "100_Applications -> 0_Interviews -> Self_Doubt -> Mental_Crash -> Study_Focus_Loss",
    "Tuition Hike": "International_Fees_Rise -> Extra_Shift_at_Job -> 4am_Bedtime -> Brain_Fog -> Quiz_Failure",

    # Random Hardship
    "CRA Scam": "Fake_CRA_Call -> Panic_State -> Scammed_Money -> Savings_Drain -> Mental_Breakdown",
    "Healthcare Delay": "ER_Wait_10hrs -> Condition_Worsens -> Miss_Project_Deadline -> Grade_Penalty"
}


def build_flexible_graph(text):
    G = nx.DiGraph()
    steps = [s.strip().replace("_", " ") for s in text.split("->")]
    for i in range(len(steps) - 1):
        G.add_edge(steps[i], steps[i+1])
    return G

def render_graph_html(G):
    net = Network(height="400px", width="100%", bgcolor="rgba(0,0,0,0)", font_color="#386939", directed=True)
    for node in G.nodes():
        net.add_node(node, label=node, color="#386939", size=20, font={'color': 'white'})
    for u, v in G.edges():
        net.add_edge(u, v, color="#93A989")
    net.save_graph("temp_graph.html")
    return open("temp_graph.html", 'r', encoding='utf-8').read()


with st.sidebar:
    st.markdown("### 🌲 Task Manager")
    with st.form("add_task_form"):
        t_title = st.text_input("Task Title")
        t_deadline = st.date_input("Deadline", datetime.now() + timedelta(days=1))
        t_energy = st.selectbox("Energy Required", ["low", "medium", "high"])
        if st.form_submit_button("Add Task"):
            new_task = {
                "title": t_title,
                "deadline": datetime.combine(t_deadline, datetime.min.time()),
                "energy_required": t_energy
            }
            st.session_state.tasks.append(new_task)
            st.success("Task Added!")

    st.divider()
    clean_options = list(TORONTO_KNOWLEDGE_BASE.keys())
    selected_display = st.selectbox("Select Scenario", ["🔍 Search"] + clean_options)

# --- 7. Main Content ---
st.title("🇨🇦 MapleRadar")

TASK_FAILURE_LOGIC = {
    "Assignment": "Miss_Deadline -> Grade_Drop -> Academic_Probation -> Visa_Risk",
    "Rent": "Late_Payment -> Landlord_Warning -> Eviction_Notice -> Homelessness",
    "Work": "Miss_Shift -> Manager_Displeasure -> Job_Loss -> Financial_Crisis",
    "Default": "Task_Incomplete -> Stress_Increase -> Productivity_Loss -> Burnout"
}

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📡 Live Toronto Pulse")
    live_c1, live_c2 = st.columns([1, 2])
    with live_c1:
        if st.button("🔄 Sync Live Data", use_container_width=True):
        
            import random
            live_events = [
                {"type": "Weather", "desc": "Extreme Cold Alert (-20°C)", "effect": "Low_Energy", "chain": "Severe_Cold -> Heating_Usage_Up -> Hydro_Bill_Surge -> Financial_Stress"},
                {"type": "TTC", "desc": "Line 1 Subway Delay", "effect": "Time_Lost", "chain": "Signal_Issues -> Subway_Stop -> 1hr_Delay -> Late_for_Commitment"},
                {"type": "Economic", "desc": "Food Price Index Up 5%", "effect": "Budget_Squeeze", "chain": "Supply_Chain_Issue -> Grocery_Cost_Up -> Less_Savings -> Anxiety"}
            ]
            selected_event = random.choice(live_events)
            st.session_state.current_live_event = selected_event
            
            
            if selected_event["type"] == "TTC":
                st.session_state.user_state["available_time"] = max(0, st.session_state.user_state["available_time"] - 60)
            elif selected_event["type"] == "Weather":
                st.session_state.user_state["energy_val"] = max(0, st.session_state.user_state["energy_val"] - 2)
            
            st.rerun()

    with live_c2:
        if "current_live_event" in st.session_state:
            ev = st.session_state.current_live_event
            st.info(f"**{ev['type']}**: {ev['desc']} (Impact: {ev['effect']})")
        else:
            st.caption("Waiting for real-time synchronization...")

    st.divider()

    user_input = st.text_input("Search a situation...", placeholder="e.g. Rent, TTC...", key="main_search").strip().lower()
    
    final_logic = ""
    is_task_risk = False
    

    if "failure_chain" in st.session_state and st.session_state.failure_chain:
        final_logic = st.session_state.failure_chain
        is_task_risk = True
        st.warning("🚨 CONSEQUENCE ANALYSIS: Impact of Potential Task Failure")
        if st.button("⬅️ Back to Global Scenarios"):
            st.session_state.failure_chain = None
            st.rerun()
    elif user_input:
        match = next((val for key, val in TORONTO_KNOWLEDGE_BASE.items() 
                     if user_input in key.lower() or user_input in val.lower()), None)
        final_logic = match
        if not final_logic:
            st.error(f"No results found for '{user_input}'.")
    elif selected_display != "🔍 Search":
        final_logic = TORONTO_KNOWLEDGE_BASE.get(selected_display)
    elif "current_live_event" in st.session_state:
        final_logic = st.session_state.current_live_event["chain"]

    if final_logic:
        current_scenario = next((k for k, v in TORONTO_KNOWLEDGE_BASE.items() if v == final_logic), "Live System Update")
        st.subheader(f"Analyzing: {current_scenario}")
        
        if st.button("🚨 Simulate Impact", use_container_width=True):
            apply_effect(final_logic)
            st.toast("System State Updated via Logic Chain!", icon="🍁")

        G = nx.DiGraph()
        steps = [s.strip().replace("_", " ") for s in final_logic.split("->")]
        for i in range(len(steps) - 1):
            G.add_edge(steps[i], steps[i+1])
        
        components.html(render_graph_html(G), height=450)
    else:
        st.info("👋 Welcome! Use 'Sync Live Data' to fetch real Toronto conditions or search a scenario.")

with col2:
    st.subheader("Survival Analytics")
    s = st.session_state.user_state
    
    st.divider()
    st.subheader("Smart Reschedule")
    
    if st.session_state.tasks:
        scored_tasks = []
        for t in st.session_state.tasks:
            score = score_task(t, s)
            scored_tasks.append((score, t))
        
        scored_tasks.sort(key=lambda x: x[0], reverse=True)
        
        for score, t in scored_tasks:
            is_overdue = t['deadline'] < datetime.now()
            status_icon = "❌" if is_overdue else ("🔴" if score > 0.7 else "🟡")
            
            with st.expander(f"{status_icon} {t['title']} (Priority: {score:.2f})"):
                st.write(f"**Deadline:** {t['deadline'].date()}")
                
                fail_logic = next((v for k, v in TASK_FAILURE_LOGIC.items() if k.lower() in t['title'].lower()), TASK_FAILURE_LOGIC["Default"])
                
                if is_overdue:
                    st.error("⚠️ TASK OVERDUE!")
                    if st.button("Analyze Consequence", key=f"fail_{t['title']}"):
                        st.session_state.failure_chain = fail_logic
                        st.rerun()
                else:
                    st.info("Status: Pending")
                    if st.button("Preview Failure Risk", key=f"risk_{t['title']}", help="如果此任务未完成，会触发什么连锁反应？"):
                        st.session_state.failure_chain = fail_logic
                        st.session_state.is_prediction = True 
                        st.rerun()
    else:
        st.write("No tasks to prioritize. Stay chill! ☕")