🇨🇦 MapleRadar: Toronto Survival Causality Mapping

MapleRadar is an interactive simulation and data visualization tool that maps the complex causal chains of navigating life in Toronto. From TTC service cuts to the grocery monopoly and housing crisis, this tool illustrates how urban stressors impact student mental health, academic performance, and financial stability.


The Team & Contributions
    Member 1:[shero233]: Lead Developer – Streamlit UI, NetworkX Graph Logic.
    Member 2:[alexhabbick]: Backend/Algorithm – Impact calculation and "GPA Risk" simulation.


What the Project Does
    Dynamic Scenarios: Simulates real-world events like "TTC Service Cuts" or "Loblaws Price Hikes."

    Causality Mapping: Visualizes how one urban factor (e.g., rent increase) triggers a chain reaction affecting productivity.

    Academic Risk Assessment: Tracks "GPA Risk" and "Academic Probation" status based on simulated lifestyle stressors.

    Local Knowledge Base: Uses a custom North York/Toronto dataset to provide context-aware survival tips.

Tech Stack
    Language: Python

    Frontend/UI: Streamlit

    Graph Engine: NetworkX & Pyvis


Installation & Setup
    Ensure you have Python 3.8+ installed.

1. Clone the Repository
    git clone [(https://github.com/shero233/MapleRadar)]
    cd MapleRadar
2. Environment Setup
    It is recommended to use a virtual environment:
        # Windows
        python -m venv venv
        .\venv\Scripts\activate

        # macOS/Linux
        python3 -m venv venv
        source venv/bin/activate
3. Install Dependencies
    pip install streamlit networkx pyvis matplotlib
4. Run the Application
    streamlit run app.py
