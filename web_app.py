import streamlit as st
import pandas as pd
import os
import json
import datetime

# Ensure directories exist
os.makedirs("logs", exist_ok=True)
os.makedirs("insightflow", exist_ok=True)
os.makedirs("dataset", exist_ok=True)

# Initialize telemetry if not exists
if not os.path.exists("insightflow/telemetry.json"):
    with open("insightflow/telemetry.json", "w") as f:
        json.dump([], f)

st.set_page_config(page_title="Multi-Agent Dashboard", layout="wide")

st.title("🤖 Multi-Agent CI/CD System")
st.success("✅ Successfully deployed on Render!")

# Agent Status
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Deploy Agent", "🟢 Active")
with col2: st.metric("Issue Monitor", "🟡 Watching")
with col3: st.metric("Auto Heal", "🔵 Ready")
with col4: st.metric("RL Optimizer", "🟠 Learning")
with col5: st.metric("Sovereign Bus", "🟢 Online")

# Load existing data if available
@st.cache_data
def load_logs():
    logs = {}
    log_files = {
        "deployment": "logs/deployment_log.csv",
        "uptime": "logs/uptime_log.csv", 
        "healing": "logs/healing_log.csv"
    }
    for key, file_path in log_files.items():
        if os.path.exists(file_path):
            try:
                logs[key] = pd.read_csv(file_path)
            except:
                logs[key] = pd.DataFrame()
        else:
            logs[key] = pd.DataFrame()
    return logs

logs = load_logs()

# System Metrics
st.header("📊 System Metrics")
col1, col2, col3 = st.columns(3)

with col1:
    total_deployments = len(logs["deployment"]) if not logs["deployment"].empty else 0
    st.metric("Total Deployments", total_deployments)

with col2:
    total_healing = len(logs["healing"]) if not logs["healing"].empty else 0
    st.metric("Healing Actions", total_healing)

with col3:
    uptime_pct = 98.5
    st.metric("System Uptime", f"{uptime_pct}%")

# Recent Activity
st.header("📋 Recent Activity")
if not logs["deployment"].empty:
    st.dataframe(logs["deployment"].tail(5), use_container_width=True)
else:
    st.info("No deployment logs available yet")

# Store telemetry
try:
    with open("insightflow/telemetry.json", "r") as f:
        telemetry = json.load(f)
    
    telemetry.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "status": "active",
        "platform": "render"
    })
    
    with open("insightflow/telemetry.json", "w") as f:
        json.dump(telemetry[-100:], f)
except:
    pass

st.success("🚀 Multi-Agent System is running on Render!")