# 🇨🇦 MapleRadar: Toronto Survival Causality Mapping

**MapleRadar** is an interactive data visualization tool built with Streamlit. It maps the complex causal chains of living in Toronto—illustrating how factors like the housing crisis, transit delays, and inflation impact student life, mental health, and academic success.

## 🚀 Quick Start (Local Setup)

If you are working from your `F:/MapleRadar` directory, follow these steps to run the application:

### 1. Navigate to the Project
Open your terminal and switch to your F drive:
```bash
F:
cd MapleRadar

# 2. Activate your virtual environment
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# 3. install required library
# run the folowing code
pip install streamlit networkx pyvis

# 4. run this file
streamlit run app.py

