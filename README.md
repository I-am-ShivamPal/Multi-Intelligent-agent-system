# Multi-Agent CI/CD System with RL Optimization

A production-ready multi-agent system that simulates CI/CD operations with intelligent self-healing capabilities, reinforcement learning optimization, and real-time monitoring.

## 🏗️ System Architecture

### Core Agents

1. **Deploy Agent** (`agents/deploy_agent.py`)
   - Manages deployment operations
   - Publishes events to sovereign bus
   - Tracks success/failure rates and response times

2. **Issue Detector Agent** (`agents/issue_detector.py`)
   - Monitors system for anomalies and failures
   - Detects data quality issues (low scores, health anomalies)
   - Identifies deployment failures and latency issues
   - Uses configurable thresholds from `config.py`

3. **Uptime Monitor Agent** (`agents/uptime_monitor.py`)
   - Tracks system uptime/downtime status
   - Maintains timeline of status changes
   - Publishes system state changes to bus

4. **Auto-Heal Agent** (`agents/auto_heal_agent.py`)
   - Executes healing strategies:
     - Retry deployment
     - Restore previous version
     - Adjust thresholds
   - Logs all healing attempts

5. **RL Optimizer Agent** (`agents/rl_optimizer.py`)
   - Implements lightweight Q-learning
   - Learns optimal healing strategies
   - Incorporates user feedback
   - Maintains Q-table for policy optimization

### Event-Driven Architecture

- **Sovereign Bus** (`core/sovereign_bus.py`): Central event distribution
- **MCP Integration** (`core/mcp_bridge.py`): Team collaboration layer
- **Real-time Telemetry** (`insightflow/`): Live monitoring and analytics
- **Enhanced Dashboard** (`dashboard/dashboard.py`): InsightFlow visualization

## 🚀 Quick Start

### Docker Deployment (Recommended)

```bash
# Start all services with Docker
./docker-start.sh  # Linux/Mac
docker-start.bat   # Windows

# Or manually
docker-compose up --build -d
```

### Local Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```bash
# Normal deployment with RL optimization
python main.py --dataset dataset/student_scores.csv --planner rl

# Patient health monitoring
python main.py --dataset dataset/patient_health.csv --planner rl

# Force anomaly testing
python main.py --dataset dataset/student_scores.csv --force-anomaly --planner rl
```

### Run Test Suite

```bash
python test_system.py
```

### Train RL Agent (10 scenarios)

```bash
python train_rl.py
```

### View Learned Strategies

```bash
python show_qtable.py
```

### Launch Enhanced Dashboard

```bash
# Enhanced dashboard with real-time features
python run_enhanced_dashboard.py

# Or standard Streamlit launch
streamlit run dashboard/dashboard.py
```

### Real-time Monitoring

```bash
# Monitor live events
python monitor_bus.py

# Start MCP endpoints for team integration
python mcp_endpoints.py

# Quick system validation
python quick_validation.py
```

## 📊 Features Demonstrated

### Day 1: Modularization + Issue Detection ✅
- ✅ Clean agent modules in `/agents` folder
- ✅ Deploy agent writes to `deployment_log.csv`
- ✅ Issue detector flags anomalies (failed deploys, high latency)
- ✅ Uptime monitor logs downtime to `uptime_log.csv`

### Day 2: Auto-Heal Agent ✅
- ✅ Self-healing strategies implementation
- ✅ Error-specific fix actions (retry, rollback, adjust)
- ✅ Healing attempts logged to `healing_log.csv`
- ✅ Integration with Issue Detector

### Day 3: RL Optimization + User Feedback ✅
- ✅ Lightweight Q-Learning implementation
- ✅ State-Action-Reward learning loop
- ✅ User feedback integration (`user_feedback_log.csv`)
- ✅ Policy learning across multiple runs

### Day 4: Complete System + Dashboard ✅
- ✅ Master orchestrator (`main.py`)
- ✅ Enhanced Streamlit dashboard with:
  - Real-time agent status monitoring
  - InsightFlow analytics (Uptime %, Heal Success, RL Rewards)
  - Developer/User mode toggle
  - Performance metrics and trends
  - Agent intelligence visualization
  - System health summary
  - RL analytics with Q-table heatmaps
  - Raw data logs

### Day 5: Event-Driven Architecture + MCP Integration ✅
- ✅ Sovereign bus for cross-process communication
- ✅ MCP bridge for team collaboration
- ✅ Real-time telemetry collection
- ✅ WebSocket server for live updates
- ✅ HTTP endpoints for external integration
- ✅ File-based event persistence

### Day 6: Containerization + Infrastructure ✅
- ✅ Docker containerization for all services
- ✅ Multi-service orchestration with docker-compose
- ✅ Environment-based configuration (.env)
- ✅ Persistent volumes for data and logs
- ✅ Cross-platform deployment scripts
- ✅ Production-ready infrastructure setup

## 🎯 Key Learning Outcomes

1. **Anomaly Detection**: Statistical thresholds for data quality
2. **Self-Healing**: Automated recovery strategies
3. **Reinforcement Learning**: Q-learning for strategy optimization
4. **User Feedback**: Human-in-the-loop learning
5. **System Integration**: Multi-agent coordination
6. **Event-Driven Architecture**: Scalable cross-process communication
7. **Real-time Monitoring**: Live system observability
8. **Team Collaboration**: Interface design and integration patterns
9. **Containerization**: Production-ready deployment with Docker
10. **Infrastructure as Code**: Orchestrated multi-service architecture

## 📈 Enhanced Dashboard Features

### Real-time Monitoring
- **Live Agent Status**: 5 agents with color-coded indicators
- **Auto-refresh**: Optional 5-second polling
- **Event Stream**: Real-time bus event monitoring

### InsightFlow Analytics
- **Uptime %**: System availability with trend charts
- **Heal Success**: Success rate tracking with improvement curves
- **RL Rewards**: Reinforcement learning performance trends

### Dual Mode Interface
- **User Mode**: Clean performance summary for stakeholders
- **Developer Mode**: Full access to logs, telemetry, and raw data

### Data Visualization
- **Performance Timeline**: Data quality trends with deployment markers
- **Agent Intelligence**: Healing success rates and strategy effectiveness
- **System Health**: Uptime percentage and error breakdowns
- **RL Analytics**: Q-table heatmaps and reward trends
- **Raw Logs**: Complete audit trail with filtering

## 🔧 Configuration

Edit `config.py` to adjust detection thresholds:

```python
THRESHOLDS = {
    "latency_ms": 24000,        # Deployment latency limit
    "low_score_avg": 40,        # Student score threshold
    "high_heart_rate": 120,     # Patient health limits
    "low_oxygen_level": 95
}
```

## 📝 Data Sources

### CSV Logs
- `logs/deployment_log.csv`: All deployment events
- `logs/uptime_log.csv`: System status timeline
- `logs/healing_log.csv`: Self-healing attempts
- `logs/issue_log.csv`: Detected problems
- `logs/rl_log.csv`: Q-table state
- `logs/rl_performance_log.csv`: Learning progress
- `logs/user_feedback_log.csv`: Human feedback

### Real-time Data
- `bus_events.json`: Cross-process event stream
- `mcp_outbox.json`: MCP integration messages
- `insightflow/telemetry.json`: Dashboard telemetry

### Integration Endpoints
- `GET /mcp_outbox`: Live message feed
- `POST /mcp_inbox`: External message input
- `GET /health`: System health check

## 🎮 Interactive Features

### Dashboard Controls
- **Mode Toggle**: Switch between User/Developer views
- **Auto-refresh**: Enable/disable real-time updates
- **Manual Refresh**: On-demand data reload
- **Supervisor Overrides**: Manual system controls

### Real-time Monitoring
- **Live Event Stream**: Bus monitor with real-time events
- **Agent Status**: Color-coded health indicators
- **Performance Metrics**: Live charts and trends
- **Telemetry Collection**: Automatic usage analytics

### Team Integration
- **MCP Endpoints**: HTTP API for external tools
- **WebSocket Server**: Real-time dashboard updates
- **Context IDs**: Unique message tracking

## 🧠 RL Learning Process

1. **State**: Current failure type (deployment_failure, latency_issue, etc.)
2. **Action**: Healing strategy (retry, restore, adjust)
3. **Reward**: +1 (success), -1 (failure), +bonus (user acceptance)
4. **Learning**: Q-table updates using temporal difference learning

The system learns optimal strategies over multiple runs, incorporating both system outcomes and user preferences.

## 🐳 Containerization

### Services
- **agents**: Core multi-agent system (main.py)
- **dashboard**: Streamlit UI on port 8501
- **mcp-endpoints**: HTTP API on port 8080

### Environment Variables
- Configure via `.env` file
- Override with `docker-compose.override.yml`
- Persistent volumes for logs and data

## 🏆 Success Metrics

- **Uptime Percentage**: System availability (95%+ target)
- **Healing Success Rate**: Recovery effectiveness (80%+ target)
- **RL Convergence**: Policy optimization over time
- **User Satisfaction**: Feedback acceptance rates
- **Event Processing**: Real-time bus throughput
- **Integration Health**: MCP sync status

## 🚀 Production Deployment

### System Validation
```bash
# Run complete system validation
python quick_validation.py

# Expected output: 5/5 components working
# Status: 🟢 SYSTEM IS PRODUCTION READY
```

### Architecture Benefits
- **Event-Driven**: Scalable cross-process communication
- **Real-time**: Live monitoring and instant feedback
- **Intelligent**: Self-healing with RL optimization
- **Collaborative**: MCP integration for team workflows
- **Observable**: Comprehensive telemetry and analytics

This system demonstrates a complete CI/CD automation pipeline with intelligent self-healing, continuous learning, and production-ready monitoring capabilities.

## 📋 Additional Documentation

- **[REFLECTION.md](REFLECTION.md)**: Team collaboration notes and personal project reflection
- **[deployment_cycle_summary.md](deployment_cycle_summary.md)**: Complete system validation results