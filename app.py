import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components


st.set_page_config(page_title="MapleRadar", layout="wide")


st.markdown("""
<style>
    [data-testid="stAppViewContainer"] {
        background-color: transparent;
    }
    [data-testid="stSidebar"] {
        background-color: transparent;
    }
    [data-testid="stTextArea"] textarea, [data-testid="stTextInput"] input {
        background-color: transparent !important;
        color: inherit !important;
        border: 1px solid rgba(49, 51, 63, 0.2) !important;
    }
    .block-container {
        background: transparent;
        padding: 6rem 1rem 10rem;
    }
    header {visibility: visible;}
</style>
""", unsafe_allow_html=True)

TORONTO_KNOWLEDGE_BASE = {
    "Housing Crisis": "Rent_+$400 -> Move_to_North_York -> 3hr_Daily_Commute -> Study_Time_Cut -> GPA_Risk",
    "Loblaws Inflation": "Loblaws_Price_Spike -> Switch_to_NoFrills -> 2hr_Travel -> Miss_Morning_Class -> Attendance_Warning",
    "TTC Service Cut": "TTC_Delay -> Late_for_Work -> Wage_Deduction -> Can't_Pay_Phone_Bill -> Mental_Stress",
    "Job Market Struggle": "Fewer_Part-time_Jobs -> Credit_Card_Debt -> High_Interest -> Debt_Spiral",
    "Winter Heating": "Hydro_Bill_Surge -> Cut_Heating -> Get_Sick -> Miss_Midterm -> Academic_Probation",
    "Food Bank Reliance": "Grocery_Cost_Rising -> Paycheck_Shortfall -> Visit_Food_Bank -> Social_Anxiety -> Mental_Burnout",
    "Scam Risk": "Cheap_Listing_Found -> Pay_Deposit -> Ghosted_by_Landlord -> Lose_1500_CAD -> Emergency_Crisis",
    "TTC Signal Issues": "Signal_Failure -> Subway_Stops -> Miss_Exam -> Late_Submission_Penalty -> Grade_Drop",
    "Phone Bill": "Data_Overage -> Rogers_Bill_Surge -> Cut_Dining_Budget -> Social_Isolation -> Depression",
    "Night Shift": "Rent_Pressure -> Overnight_Shift -> Sleep_Deprivation -> Brain_Fog -> Quiz_Failure",
    "Rent Trap": "2k rent -> income gap -> no savings -> stuck forever",
    "Rent Turnover": "move out -> new rent -> 44 percentage higher -> regret move",
    "Luxury Supply": "new condos -> high prices -> no affordability -> forced sharing",
    "Loblaws Inflation (Alt)": "price jump -> smaller basket -> poor diet -> low energy",
    "Food Cut Cycle": "skip groceries -> cheap carbs -> health drop -> sick days",
    "TTC Delay Chain": "signal delay -> late class -> missed content -> grade drop",
    "TTC Commute": "long commute -> daily fatigue -> no study -> GPA fall",
    "Job Market": "high youth unemployment -> no offers -> savings drain -> panic mode",
    "Resume Void": "apply jobs -> zero replies -> self doubt -> mental crash",
    "Overwork Loop": "two jobs -> no sleep -> burnout hit -> deadline miss",
    "Winter Heating (Alt)": "cold winter -> heating surge -> bill stress -> sleep loss",
    "Library Night": "all night study -> 3h sleep -> miss alarm -> exam fail",
    "Rent Income Gap": "2.2k rent -> 88k needed -> reality gap -> constant stress",
    "Roommate Shift": "rent too high -> find roommates -> no privacy -> mental drain",
    "Migration Drop": "policy cuts -> fewer students -> job scarcity -> income stress",
    "Currency Pressure": "weak currency -> higher CAD cost -> budget break -> daily anxiety",
    "CRA Scam": "fake CRA call -> fear spike -> money sent -> regret spiral",
    "Rental Scam": "fake listing -> deposit paid -> ghost landlord -> housing crisis",
    "Food Bank Loop": "empty wallet -> food bank -> shame feeling -> isolation grows",
    "Burnout City": "high cost city -> constant stress -> no rest -> motivation gone",
    "Tax Rent Shift": "tax increase -> landlord cost -> rent pass -> tenant stress",
    "Fare Freeze Illusion": "fare freeze -> still delays -> late commute -> job risk",
    "Transit Cap Trap": "fare cap -> forced rides -> long commute -> time drain",
    "Grocery Inflation": "food inflation -> smaller basket -> nutrition drop -> fatigue",
    "Import Dependency": "import reliance -> price spikes -> grocery stress -> diet cuts",
    "Student Food Program": "free meals -> basic relief -> still hungry -> focus loss",
    "Library Hours": "longer hours -> late nights -> sleep debt -> burnout hit",
    "Rent Supply Gap": "new housing -> still expensive -> no access -> shared living",
    "Inflation Cooling": "inflation slows -> costs still high -> wage gap -> constant stress",
    "Energy Risk": "oil price spike -> transport cost -> food price -> budget break"
}


def build_flexible_graph(text):
    G = nx.DiGraph()
    clean_text = text.replace("_", " ")
    lines = clean_text.replace("->", "→").split("\n")
    for line in lines:
        steps = [s.strip() for s in line.split("→") if s.strip()]
        if len(steps) > 1:
            for i in range(len(steps) - 1):
                G.add_edge(steps[i], steps[i+1])
    return G

def render_graph_html(G):
    net = Network(height="550px", width="100%", bgcolor="rgba(0,0,0,0)", font_color="#386939", directed=True)

    for node in G.nodes():
        is_root = G.in_degree(node) == 0
        is_end = G.out_degree(node) == 0
        color = "#386939" if is_root else ("#123418" if is_end else "#93A989")

        net.add_node(
            node,
            label=node,
            color=color,
            size=25,
            font={'size': 14, 'face': 'Arial', 'color': 'white' if is_end else '#386939'}
        )

    for u, v in G.edges():
        net.add_edge(u, v, color="#93A989", width=2)

    net.set_options("""
    var options = {
      nodes: { shadow: true },
      edges: { smooth: true },
      physics: { stabilization: true }
    }
    """)

    net.save_graph("temp_graph.html")
    return open("temp_graph.html", 'r', encoding='utf-8').read()

# --- 5. Sidebar ---
with st.sidebar:
    st.markdown("### 🌲 MapleRadar")
    st.markdown("Toronto Survival Causality")

    clean_options = [k.replace("_", " ") for k in TORONTO_KNOWLEDGE_BASE.keys()]
    option_mapping = {k.replace("_", " "): k for k in TORONTO_KNOWLEDGE_BASE.keys()}

    selected_display = st.selectbox("Quick Selection", ["🔍 Smart Search"] + clean_options)

    st.divider()
    st.markdown(f"**Status:** Online")
    st.markdown(f"**Database:** 40 Chains")

st.title("🇨🇦 MapleRadar")
st.markdown("<p style='color: #6A7B6A;'>Navigating Toronto's Complexity with Causal Intelligence</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2.5, 1])

with col1:
    user_input = st.text_input("Search a situation...", placeholder="e.g. Rent, TTC, Job...", label_visibility="collapsed").lower()

    final_logic = ""
    if user_input:
        match = next((val for key, val in TORONTO_KNOWLEDGE_BASE.items()
                      if user_input in key.lower() or user_input in val.lower()), None)
        final_logic = match if match else (user_input if "->" in user_input else "")
    elif selected_display != "🔍 Smart Search":
        final_logic = TORONTO_KNOWLEDGE_BASE[option_mapping[selected_display]]

    if final_logic:
        G = build_flexible_graph(final_logic)
        html_data = render_graph_html(G)
        components.html(html_data, height=600)
    else:
        st.markdown("### Ready to Analyze")

with col2:
    st.subheader("Survival Analytics")

    risk_level = "Monitor"
    if final_logic:
        if any(k in final_logic.lower() for k in ["gpa", "scam", "debt", "crisis", "fail"]):
            risk_level = "CRITICAL"
        elif any(k in final_logic.lower() for k in ["delay", "inflation", "bill", "stress"]):
            risk_level = "WARNING"

    st.metric("Risk Level", risk_level)