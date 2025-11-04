import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
import datetime
import time
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="InsightFlow Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Telemetry Functions ---
@st.cache_data(ttl=2)
def load_telemetry():
    try:
        with open("insightflow/telemetry.json", 'r') as f:
            return json.load(f)
    except:
        return []

def store_telemetry(entry):
    try:
        telemetry = load_telemetry()
        telemetry.append(entry)
        if len(telemetry) > 1000:
            telemetry = telemetry[-1000:]
        with open("insightflow/telemetry.json", 'w') as f:
            json.dump(telemetry, f, indent=2)
    except:
        pass

# --- Data Loading ---
@st.cache_data(ttl=5)
def load_data():
    data = {}
    files = {
        "deploy_log": "logs/deployment_log.csv",
        "uptime": "logs/uptime_log.csv",
        "healing_log": "logs/healing_log.csv",
        "q_table": "logs/rl_log.csv",
        "scores": "dataset/student_scores.csv",
        "health": "dataset/patient_health.csv",
        "feedback": "logs/user_feedback_log.csv",
        "issue_log": "logs/issue_log.csv",
        "reward_trend": "logs/rl_performance_log.csv",
        "supervisor_override": "logs/supervisor_override_log.csv"
    }
    for key, filename in files.items():
        if os.path.exists(filename):
            try:
                if key == "q_table":
                    data[key] = pd.read_csv(filename, index_col=0)
                else:
                    data[key] = pd.read_csv(filename)
            except Exception as e:
                st.error(f"Error loading {filename}: {str(e)}")
                data[key] = pd.DataFrame()
        else:
            data[key] = pd.DataFrame()
    return data

# --- Load Data ---
data_frames = load_data()
deploy_log_df = data_frames["deploy_log"]
uptime_df = data_frames["uptime"]
healing_log_df = data_frames["healing_log"]
q_table_df = data_frames["q_table"]
scores_df = data_frames["scores"]
health_df = data_frames["health"]
feedback_df = data_frames["feedback"]
issue_log_df = data_frames["issue_log"]
reward_trend_df = data_frames.get("reward_trend", pd.DataFrame())
supervisor_override_df = data_frames.get("supervisor_override", pd.DataFrame())

# Convert timestamps
for df in [scores_df, health_df, deploy_log_df, uptime_df, healing_log_df, feedback_df, issue_log_df, reward_trend_df, supervisor_override_df]:
    if not df.empty and 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# --- SIDEBAR ---
st.sidebar.header("Dashboard Controls ⚙️")

# Mode Toggle
view_mode = st.sidebar.radio("View Mode", ["User Mode", "Developer Mode"])
auto_refresh = st.sidebar.checkbox("Auto Refresh (5s)", value=False)

performance_view = st.sidebar.selectbox(
    "Performance View:",
    ["Student Scores", "Patient Health"]
)

st.sidebar.subheader("Supervisor Override")
manual_action = st.sidebar.selectbox("Action:", ["None", "Force Heal", "Force Restart"])
if st.sidebar.button("Apply Override"):
    override_entry = {
        'timestamp': pd.Timestamp.now(),
        'event_type': 'Manual Override',
        'status': manual_action,
        'details': 'Supervisor action'
    }
    override_df = pd.DataFrame([override_entry])
    override_df.to_csv("logs/supervisor_override_log.csv", mode='a', 
                      header=not os.path.exists("logs/supervisor_override_log.csv"), index=False)
    st.sidebar.success(f"Override '{manual_action}' applied")

# --- MAIN DASHBOARD ---
st.title("🔍 InsightFlow Dashboard")

# Agent Status Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1: st.metric("Deploy Agent", "🟢 Active")
with col2: st.metric("Issue Monitor", "🟡 Watching")
with col3: st.metric("Auto Heal", "🔵 Ready")
with col4: st.metric("RL Optimizer", "🟠 Learning")
with col5: st.metric("Sovereign Bus", "🟢 Online")

# Auto refresh
if auto_refresh:
    time.sleep(5)
    st.rerun()

if st.button("🔄 Manual Refresh"):
    st.rerun()

# InsightFlow Analytics
st.header("📊 InsightFlow Analytics")
insight_col1, insight_col2, insight_col3 = st.columns(3)

with insight_col1:
    st.subheader("Uptime %")
    uptime_pct = 95.5 if not uptime_df.empty else 100.0
    st.metric("System Uptime", f"{uptime_pct}%", delta="2.1%")

with insight_col2:
    st.subheader("Heal Success")
    if not healing_log_df.empty:
        success_rate = (healing_log_df['status'] == 'success').mean() * 100
        st.metric("Success Rate", f"{success_rate:.1f}%")
    else:
        st.metric("Success Rate", "N/A")

with insight_col3:
    st.subheader("RL Rewards")
    if not reward_trend_df.empty:
        avg_reward = reward_trend_df['reward'].mean()
        st.metric("Avg Reward", f"{avg_reward:.2f}")
    else:
        st.metric("Avg Reward", "N/A")

# Main Tabs
if view_mode == "Developer Mode":
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Performance & Events", 
        "🧠 Agent Intelligence", 
        "🩺 System Health", 
        "🎯 RL Analytics", 
        "📂 Raw Data Logs"
    ])
else:
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Performance Summary", 
        "🩺 System Health", 
        "📈 Key Metrics", 
        "ℹ️ Info", 
        "ℹ️ Info"
    ])

# TAB 1: Performance & Events
with tab1:
    st.header(f"{performance_view} Performance")
    
    if performance_view == "Student Scores":
        if not scores_df.empty and 'timestamp' in scores_df.columns:
            try:
                avg_scores = scores_df.groupby(scores_df['timestamp'].dt.date)['score'].mean().reset_index()
                fig = px.line(avg_scores, x='timestamp', y='score', markers=True,
                             title="Student Score Trends", template="plotly_dark")
                
                # Add deployment markers
                for _, row in deploy_log_df.iterrows():
                    if pd.notna(row['timestamp']):
                        color = "green" if row.get('status') == 'success' else "red"
                        fig.add_vline(x=str(row['timestamp'].date()), 
                                    line_width=2, line_dash="dash", line_color=color)
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error plotting scores: {str(e)}")
        else:
            st.warning("Student scores data not available")
    
    elif performance_view == "Patient Health":
        if not health_df.empty and 'timestamp' in health_df.columns:
            try:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Heart Rate")
                    fig_hr = px.line(health_df, x='timestamp', y='heart_rate', 
                                   markers=True, template="plotly_dark")
                    st.plotly_chart(fig_hr, use_container_width=True)
                
                with col2:
                    st.subheader("Oxygen Level")
                    fig_o2 = px.line(health_df, x='timestamp', y='oxygen_level', 
                                   markers=True, template="plotly_dark")
                    st.plotly_chart(fig_o2, use_container_width=True)
            except Exception as e:
                st.error(f"Error plotting health data: {str(e)}")
        else:
            st.warning("Patient health data not available")
    
    # Event Timeline
    st.header("Event Timeline")
    try:
        logs_to_combine = []
        if not deploy_log_df.empty: 
            logs_to_combine.append(deploy_log_df.assign(source='Deploy'))
        if not uptime_df.empty: 
            logs_to_combine.append(uptime_df.assign(source='Uptime'))
        if not healing_log_df.empty: 
            logs_to_combine.append(healing_log_df.assign(source='Healing'))
        if not issue_log_df.empty: 
            logs_to_combine.append(issue_log_df.assign(source='Issues'))
        
        if logs_to_combine:
            all_logs = pd.concat(logs_to_combine, ignore_index=True, sort=False)
            all_logs = all_logs.sort_values('timestamp', ascending=False)
            st.dataframe(all_logs.head(20), use_container_width=True)
        else:
            st.info("No event data available")
    except Exception as e:
        st.error(f"Error combining logs: {str(e)}")

# TAB 2: Agent Intelligence
with tab2:
    st.header("🧠 Healing Agent Performance")
    
    if not healing_log_df.empty:
        try:
            total_attempts = len(healing_log_df)
            success_count = (healing_log_df['status'] == 'success').sum()
            success_rate = success_count / total_attempts * 100
            
            col1, col2, col3 = st.columns(3)
            with col1: st.metric("Total Attempts", total_attempts)
            with col2: st.metric("Success Rate", f"{success_rate:.1f}%")
            with col3: st.metric("Successful Heals", success_count)
            
            # Success/Failure Pie Chart
            st.subheader("Success Distribution")
            fail_count = total_attempts - success_count
            fig_pie = px.pie(
                names=["Success", "Failure"],
                values=[success_count, fail_count],
                title="Healing Outcomes"
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
            # Learning Progress
            if len(healing_log_df) > 1:
                st.subheader("Learning Progress")
                healing_log_df['cumulative_success'] = (
                    (healing_log_df['status'] == 'success').cumsum() / 
                    (healing_log_df.index + 1) * 100
                )
                fig_progress = px.line(
                    healing_log_df.reset_index(), 
                    x='index', 
                    y='cumulative_success',
                    title="Success Rate Over Time",
                    markers=True
                )
                st.plotly_chart(fig_progress, use_container_width=True)
        except Exception as e:
            st.error(f"Error analyzing healing data: {str(e)}")
    else:
        st.info("No healing data available yet")

# TAB 3: System Health
with tab3:
    st.header("🩺 System Health Summary")
    
    # Calculate metrics
    try:
        uptime_percent = 100.0
        if not uptime_df.empty and len(uptime_df) > 1:
            up_count = (uptime_df['status'] == 'UP').sum()
            uptime_percent = up_count / len(uptime_df) * 100
        
        total_errors = len(issue_log_df) if not issue_log_df.empty else 0
        total_fixes = len(healing_log_df) if not healing_log_df.empty else 0
        
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Uptime", f"{uptime_percent:.1f}%")
        with col2: st.metric("Errors Detected", total_errors)
        with col3: st.metric("Fix Actions", total_fixes)
        
        # Error Breakdown
        st.subheader("Error Types")
        if not issue_log_df.empty and 'failure_state' in issue_log_df.columns:
            error_counts = issue_log_df['failure_state'].value_counts()
            fig_errors = px.bar(
                x=error_counts.index, 
                y=error_counts.values,
                title="Error Type Distribution"
            )
            st.plotly_chart(fig_errors, use_container_width=True)
        else:
            st.info("No error data available")
        
        # Healing Strategies
        st.subheader("Healing Strategies")
        if not healing_log_df.empty and 'strategy' in healing_log_df.columns:
            strategy_counts = healing_log_df['strategy'].value_counts()
            fig_strategies = px.bar(
                x=strategy_counts.index, 
                y=strategy_counts.values,
                title="Healing Strategy Usage"
            )
            st.plotly_chart(fig_strategies, use_container_width=True)
        else:
            st.info("No healing strategy data available")
            
    except Exception as e:
        st.error(f"Error calculating health metrics: {str(e)}")

# TAB 4: RL Analytics
with tab4:
    if view_mode == "Developer Mode":
        st.header("🎯 RL Analytics")
        
        # Q-Table Display
        st.subheader("Q-Table Heatmap")
        if not q_table_df.empty:
            try:
                st.info("Q-values: Higher values (brighter) indicate better learned strategies")
                st.dataframe(
                    q_table_df.style.background_gradient(cmap='viridis').format("{:.3f}"),
                    use_container_width=True
                )
                
                # Q-Table as heatmap
                fig_q = px.imshow(
                    q_table_df,
                    labels=dict(x="Action", y="State", color="Q-Value"),
                    color_continuous_scale='viridis',
                    title="Q-Table Heatmap"
                )
                st.plotly_chart(fig_q, use_container_width=True)
            except Exception as e:
                st.error(f"Error displaying Q-table: {str(e)}")
        else:
            st.warning("No Q-table data available")
        
        # Reward Trends
        st.subheader("Reward Trends")
        if not reward_trend_df.empty:
            try:
                fig_rewards = px.line(
                    reward_trend_df, 
                    x='timestamp', 
                    y='reward',
                    title="RL Reward Over Time",
                    markers=True
                )
                st.plotly_chart(fig_rewards, use_container_width=True)
            except Exception as e:
                st.error(f"Error plotting rewards: {str(e)}")
        else:
            st.info("No reward data available")
    else:
        st.info("RL Analytics available in Developer Mode")

# TAB 5: Raw Data Logs
with tab5:
    if view_mode == "Developer Mode":
        st.header("📂 Raw Data Logs")
        
        # Telemetry
        with st.expander("Recent Telemetry"):
            telemetry = load_telemetry()
            if telemetry:
                for entry in telemetry[-5:]:
                    st.json(entry)
            else:
                st.info("No telemetry data")
        
        # All logs
        log_sections = {
            "Deployment Log": deploy_log_df,
            "Uptime Log": uptime_df,
            "Healing Log": healing_log_df,
            "Issue Log": issue_log_df,
            "RL Performance": reward_trend_df,
            "User Feedback": feedback_df,
            "Supervisor Overrides": supervisor_override_df
        }
        
        for name, df in log_sections.items():
            with st.expander(f"Show {name}"):
                if not df.empty:
                    st.dataframe(df.tail(10), use_container_width=True)
                else:
                    st.info(f"No data in {name}")
    else:
        st.info("Raw logs available in Developer Mode")

# Store telemetry
store_telemetry({
    "timestamp": datetime.datetime.now().isoformat(),
    "dashboard_mode": view_mode,
    "active_users": 1,
    "system_health": "healthy"
})